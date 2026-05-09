from django.utils import timezone
from rest_framework import serializers

from apps.usuarios.models import Usuario

PHOTO_UPDATE_COOLDOWN_MONTHS = 5


def add_months(value, months):
    month = value.month - 1 + months
    year = value.year + month // 12
    month = month % 12 + 1
    day = min(
        value.day,
        [
            31,
            29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31,
        ][month - 1],
    )
    return value.replace(year=year, month=month, day=day)


class UsuarioMeSerializer(serializers.ModelSerializer):
    foto_perfil = serializers.SerializerMethodField()
    foto_perfil_upload = serializers.ImageField(write_only=True, required=False)
    foto_perfil_updated_at = serializers.SerializerMethodField()
    foto_perfil_can_update = serializers.SerializerMethodField()
    foto_perfil_next_update_at = serializers.SerializerMethodField()
    codigo_docente = serializers.SerializerMethodField()
    departamento = serializers.CharField(required=False, allow_blank=True)
    codigo_estudiante = serializers.SerializerMethodField()
    carrera = serializers.CharField(required=False, allow_blank=True)
    ciclo = serializers.IntegerField(required=False, min_value=1)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "rol",
            "foto_perfil",
            "foto_perfil_upload",
            "foto_perfil_updated_at",
            "foto_perfil_can_update",
            "foto_perfil_next_update_at",
            "codigo_docente",
            "departamento",
            "codigo_estudiante",
            "carrera",
            "ciclo",
        ]
        read_only_fields = [
            "id",
            "username",
            "rol",
            "foto_perfil",
            "foto_perfil_updated_at",
            "foto_perfil_can_update",
            "foto_perfil_next_update_at",
            "codigo_docente",
            "codigo_estudiante",
        ]

    def get_foto_perfil(self, obj):
        if obj.rol != "estudiante" or not hasattr(obj, "estudiante"):
            return None

        foto_perfil = obj.estudiante.foto_perfil
        if not foto_perfil:
            return None

        request = self.context.get("request")
        if request is None:
            return foto_perfil.url

        return request.build_absolute_uri(foto_perfil.url)

    def get_foto_perfil_updated_at(self, obj):
        estudiante = self._get_estudiante(obj)
        if estudiante is None:
            return None

        return estudiante.foto_perfil_updated_at

    def get_foto_perfil_can_update(self, obj):
        estudiante = self._get_estudiante(obj)
        if estudiante is None:
            return False

        return self._photo_can_update(estudiante)

    def get_foto_perfil_next_update_at(self, obj):
        estudiante = self._get_estudiante(obj)
        if estudiante is None or estudiante.foto_perfil_updated_at is None:
            return None

        return add_months(estudiante.foto_perfil_updated_at, PHOTO_UPDATE_COOLDOWN_MONTHS)

    def get_codigo_docente(self, obj):
        if obj.rol != "docente" or not hasattr(obj, "docente"):
            return None

        return obj.docente.codigo_docente

    def get_codigo_estudiante(self, obj):
        estudiante = self._get_estudiante(obj)
        return estudiante.codigo_estudiante if estudiante is not None else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.rol == "docente" and hasattr(instance, "docente"):
            representation["departamento"] = instance.docente.departamento
        else:
            representation["departamento"] = None

        estudiante = self._get_estudiante(instance)
        if estudiante is not None:
            representation["carrera"] = estudiante.carrera
            representation["ciclo"] = estudiante.ciclo
        else:
            representation["carrera"] = None
            representation["ciclo"] = None

        return representation

    def validate(self, attrs):
        if "foto_perfil_upload" in attrs:
            user = self.instance
            estudiante = self._get_estudiante(user)

            if estudiante is None:
                raise serializers.ValidationError(
                    {"foto_perfil_upload": "Solo los estudiantes pueden actualizar la foto."}
                )

            if not self._photo_can_update(estudiante):
                next_update = add_months(
                    estudiante.foto_perfil_updated_at, PHOTO_UPDATE_COOLDOWN_MONTHS
                )
                raise serializers.ValidationError(
                    {
                        "foto_perfil_upload": (
                            "La foto de perfil solo se puede actualizar cada 5 meses. "
                            f"Podras cambiarla nuevamente desde {next_update.date().isoformat()}."
                        )
                    }
                )

        return attrs

    def update(self, instance, validated_data):
        foto_perfil = validated_data.pop("foto_perfil_upload", None)
        carrera = validated_data.pop("carrera", None)
        ciclo = validated_data.pop("ciclo", None)
        departamento = validated_data.pop("departamento", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if instance.rol == "estudiante" and hasattr(instance, "estudiante"):
            estudiante = instance.estudiante
            if carrera is not None:
                estudiante.carrera = carrera
            if ciclo is not None:
                estudiante.ciclo = ciclo
            if foto_perfil is not None:
                estudiante.foto_perfil = foto_perfil
                estudiante.foto_perfil_updated_at = timezone.now()
            estudiante.save()

        if instance.rol == "docente" and hasattr(instance, "docente") and departamento is not None:
            instance.docente.departamento = departamento
            instance.docente.save(update_fields=["departamento"])

        return instance

    def _get_estudiante(self, obj):
        if obj.rol != "estudiante" or not hasattr(obj, "estudiante"):
            return None

        return obj.estudiante

    def _photo_can_update(self, estudiante):
        if estudiante.foto_perfil_updated_at is None:
            return True

        return timezone.now() >= add_months(
            estudiante.foto_perfil_updated_at, PHOTO_UPDATE_COOLDOWN_MONTHS
        )
