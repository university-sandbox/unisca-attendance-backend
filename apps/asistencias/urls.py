from django.urls import path

from apps.asistencias.views import ListarAsistenciaView, RegistrarAsistenciaView

urlpatterns = [
    path(
        "asistencias/",
        RegistrarAsistenciaView.as_view(),
        name="registrar-asistencia",
    ),
    path(
        "sesiones/<int:sesion_id>/asistencias/",
        ListarAsistenciaView.as_view(),
        name="listar-asistencia",
    ),
]
