from rest_framework import serializers

from apps.cursos.models import Curso, Sesion


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ["id", "nombre", "codigo", "ciclo_academico"]


class SesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sesion
        fields = ["id", "curso", "fecha_inicio", "fecha_fin", "qr_token", "activa"]
        read_only_fields = ["fecha_inicio", "qr_token"]

    def validate_curso(self, curso):
        request = self.context["request"]
        if curso.docente.usuario_id != request.user.id:
            raise serializers.ValidationError("El curso no pertenece al docente.")

        return curso
