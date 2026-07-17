from rest_framework import serializers

from apps.asistencias.models import Asistencia

FACE_VERIFICATION_DIAGNOSTIC_EVENTS = [
    "verification_started",
    "models_loaded",
    "reference_image_loaded",
    "camera_started",
    "verification_succeeded",
    "verification_failed",
]


class AsistenciaCreateSerializer(serializers.Serializer):
    qr_token = serializers.UUIDField()
    face_verified = serializers.BooleanField(required=True)

    def validate_face_verified(self, value):
        if not value:
            raise serializers.ValidationError(
                "La verificacion facial es obligatoria para registrar asistencia."
            )

        return value


class FaceVerificationDiagnosticSerializer(serializers.Serializer):
    event = serializers.ChoiceField(choices=FACE_VERIFICATION_DIAGNOSTIC_EVENTS)
    stage = serializers.CharField(max_length=64, required=False, allow_blank=True)
    client_origin = serializers.CharField(max_length=255, required=False, allow_blank=True)
    reference_image_origin = serializers.CharField(
        max_length=255, required=False, allow_blank=True
    )
    error_name = serializers.CharField(max_length=128, required=False, allow_blank=True)
    error_message = serializers.CharField(max_length=500, required=False, allow_blank=True)


class AsistenciaListSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.CharField(
        source="estudiante.usuario.get_full_name", read_only=True
    )
    estudiante_codigo = serializers.CharField(source="estudiante.codigo_estudiante", read_only=True)

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
