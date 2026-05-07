from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.usuarios.serializers import UsuarioMeSerializer


class UsuarioMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UsuarioMeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
