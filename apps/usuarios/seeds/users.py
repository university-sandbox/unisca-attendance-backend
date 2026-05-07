from django.contrib.auth import get_user_model

from apps.usuarios.models import Docente, Estudiante
from apps.usuarios.seeds.constants import DEFAULT_PASSWORD
from apps.usuarios.seeds.data import ADMIN_USERS, DOCENTES, ESTUDIANTES


def seed_users():
    users = {}

    for item in ADMIN_USERS:
        users[item["username"]] = _upsert_user(
            username=item["username"],
            email=item["email"],
            first_name=item["first_name"],
            last_name=item["last_name"],
            rol="admin",
            is_staff=True,
            is_superuser=True,
        )

    for item in DOCENTES:
        user = _upsert_user(
            username=item["username"],
            email=item["email"],
            first_name=item["first_name"],
            last_name=item["last_name"],
            rol="docente",
        )
        Docente.objects.update_or_create(
            usuario=user,
            defaults={
                "codigo_docente": item["codigo_docente"],
                "departamento": item["departamento"],
            },
        )
        users[item["username"]] = user

    for item in ESTUDIANTES:
        user = _upsert_user(
            username=item["username"],
            email=item["email"],
            first_name=item["first_name"],
            last_name=item["last_name"],
            rol="estudiante",
        )
        Estudiante.objects.update_or_create(
            usuario=user,
            defaults={
                "codigo_estudiante": item["codigo_estudiante"],
                "carrera": item["carrera"],
                "ciclo": item["ciclo"],
            },
        )
        users[item["username"]] = user

    return users


def _upsert_user(
    *,
    username,
    email,
    first_name,
    last_name,
    rol,
    is_staff=False,
    is_superuser=False,
):
    User = get_user_model()
    user, _ = User.objects.get_or_create(username=username)
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.rol = rol
    user.is_staff = is_staff
    user.is_superuser = is_superuser
    user.is_active = True
    user.set_password(DEFAULT_PASSWORD)
    user.save()
    return user
