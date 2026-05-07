from rest_framework import serializers

from apps.usuarios.models import Usuario


class UsuarioMeSerializer(serializers.ModelSerializer):
    foto_perfil = serializers.SerializerMethodField()

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
        ]
        read_only_fields = ["id", "username", "rol", "foto_perfil"]

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
