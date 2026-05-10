from django.db import IntegrityError, transaction
from django.utils import timezone
from django.utils.dateparse import parse_date
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.asistencias.models import Asistencia
from apps.asistencias.permissions import IsDocente, IsEstudiante
from apps.asistencias.serializers import (
    AsistenciaCreateSerializer,
    AsistenciaListSerializer,
)
from apps.cursos.models import Sesion


class AsistenciaPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class RegistrarAsistenciaView(generics.CreateAPIView):
    serializer_class = AsistenciaCreateSerializer
    permission_classes = [IsEstudiante]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        qr_token = serializer.validated_data["qr_token"]
        face_verified = serializer.validated_data["face_verified"]

        try:
            sesion = Sesion.objects.get(qr_token=qr_token, activa=True)
        except Sesion.DoesNotExist:
            return Response(
                {"error": "Sesion invalida o expirada."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        metodo = "qr+facial"

        try:
            with transaction.atomic():
                asistencia = Asistencia.objects.create(
                    sesion=sesion,
                    estudiante=request.user.estudiante,
                    face_verified=face_verified,
                    metodo=metodo,
                )
        except IntegrityError:
            return Response(
                {"error": "Asistencia ya registrada."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "status": "registrado",
                "timestamp": asistencia.timestamp_registro,
                "metodo": metodo,
            },
            status=status.HTTP_201_CREATED,
        )


class ListarAsistenciaView(generics.ListAPIView):
    serializer_class = AsistenciaListSerializer
    permission_classes = [IsDocente]

    def get_queryset(self):
        return Asistencia.objects.filter(
            sesion_id=self.kwargs["sesion_id"],
            sesion__curso__docente=self.request.user.docente,
        ).select_related("estudiante__usuario")


class ListarAsistenciaCursoView(generics.ListAPIView):
    serializer_class = AsistenciaListSerializer
    permission_classes = [IsDocente]
    pagination_class = AsistenciaPagination

    def get_queryset(self):
        fecha = parse_date(self.request.query_params.get("fecha", ""))

        if fecha is None:
            fecha = timezone.localdate()

        return (
            Asistencia.objects.filter(
                sesion__curso_id=self.kwargs["curso_id"],
                sesion__curso__docente=self.request.user.docente,
                timestamp_registro__date=fecha,
            )
            .select_related("estudiante__usuario")
            .order_by("-timestamp_registro", "estudiante__usuario__last_name")
        )
