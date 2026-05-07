from django.urls import path

from apps.usuarios.views import UsuarioMeView

urlpatterns = [
    path("me/", UsuarioMeView.as_view(), name="usuario-me"),
]
