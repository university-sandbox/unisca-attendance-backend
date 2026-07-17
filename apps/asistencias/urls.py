from django.urls import path

from apps.asistencias.views import (
    FaceVerificationDiagnosticView,
    ListarAsistenciaCursoView,
    ListarAsistenciaView,
    RegistrarAsistenciaView,
)

urlpatterns = [
    path(
        "asistencias/face-verification-diagnostics/",
        FaceVerificationDiagnosticView.as_view(),
        name="face-verification-diagnostics",
    ),
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
