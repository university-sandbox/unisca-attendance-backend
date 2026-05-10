from django.urls import path

from apps.asistencias.views import (
    ListarAsistenciaCursoView,
    ListarAsistenciaView,
    RegistrarAsistenciaView,
)

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
    path(
        "cursos/<int:curso_id>/asistencias/",
        ListarAsistenciaCursoView.as_view(),
        name="listar-asistencia-curso",
    ),
]
