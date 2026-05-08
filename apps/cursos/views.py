from rest_framework import viewsets

from apps.cursos.models import Curso, Sesion
from apps.cursos.permissions import IsDocente
from apps.cursos.serializers import CursoSerializer, SesionSerializer


class CursoViewSet(viewsets.ModelViewSet):
    serializer_class = CursoSerializer
    permission_classes = [IsDocente]

    def get_queryset(self):
        return Curso.objects.filter(docente=self.request.user.docente)

    def perform_create(self, serializer):
        serializer.save(docente=self.request.user.docente)


class SesionViewSet(viewsets.ModelViewSet):
    serializer_class = SesionSerializer
    permission_classes = [IsDocente]

    def get_queryset(self):
        return Sesion.objects.filter(curso__docente=self.request.user.docente).select_related(
            "curso"
        )
