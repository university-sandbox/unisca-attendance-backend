from django.contrib.auth import get_user_model
from django.db import transaction

from apps.asistencias.models import Asistencia
from apps.cursos.models import Curso, Sesion
from apps.usuarios.models import Docente, Estudiante
from apps.usuarios.seeds.attendance import seed_attendance
from apps.usuarios.seeds.courses import seed_courses
from apps.usuarios.seeds.data import (
    ADMIN_USERS,
    ASISTENCIAS,
    CURSOS,
    DOCENTES,
    ESTUDIANTES,
    SESIONES,
)
from apps.usuarios.seeds.sessions import seed_sessions
from apps.usuarios.seeds.users import seed_users


@transaction.atomic
def run_seed(*, reset=False):
    if reset:
        reset_seed_data()

    seed_users()
    cursos = seed_courses()
    sesiones = seed_sessions(cursos)
    asistencias = seed_attendance(sesiones)

    return {
        "administradores": len(ADMIN_USERS),
        "docentes": len(DOCENTES),
        "estudiantes": len(ESTUDIANTES),
        "cursos": len(cursos),
        "sesiones": len(sesiones),
        "asistencias": len(asistencias),
    }


def reset_seed_data():
    session_tokens = [item["qr_token"] for item in SESIONES]
    student_codes = [item["codigo_estudiante"] for item in ESTUDIANTES]
    teacher_codes = [item["codigo_docente"] for item in DOCENTES]
    course_codes = [item["codigo"] for item in CURSOS]
    usernames = [item["username"] for item in [*ADMIN_USERS, *DOCENTES, *ESTUDIANTES]]

    Asistencia.objects.filter(
        sesion__qr_token__in=session_tokens,
        estudiante__codigo_estudiante__in=[item["codigo_estudiante"] for item in ASISTENCIAS],
    ).delete()
    Sesion.objects.filter(qr_token__in=session_tokens).delete()
    Curso.objects.filter(codigo__in=course_codes).delete()
    Estudiante.objects.filter(codigo_estudiante__in=student_codes).delete()
    Docente.objects.filter(codigo_docente__in=teacher_codes).delete()
    Estudiante.objects.filter(usuario__username__in=usernames).delete()
    Docente.objects.filter(usuario__username__in=usernames).delete()
    get_user_model().objects.filter(username__in=usernames).delete()
