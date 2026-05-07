from rest_framework import serializers

from apps.asistencias.models import Asistencia


class AsistenciaCreateSerializer(serializers.Serializer):
    qr_token = serializers.UUIDField()
    face_verified = serializers.BooleanField(default=False)


class AsistenciaListSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.CharField(
        source="estudiante.usuario.get_full_name", read_only=True
    )
    estudiante_codigo = serializers.CharField(
        source="estudiante.codigo_estudiante", read_only=True
    )

    class Meta:
        model = Asistencia
        fields = [
            "id",
            "estudiante_nombre",
            "estudiante_codigo",
            "timestamp_registro",
            "metodo",
            "face_verified",
        ]
