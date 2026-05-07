from apps.cursos.models import Sesion
from apps.usuarios.seeds.data import SESIONES


def seed_sessions(cursos):
    sesiones = {}

    for item in SESIONES:
        sesion, _ = Sesion.objects.update_or_create(
            qr_token=item["qr_token"],
            defaults={
                "curso": cursos[item["curso_codigo"]],
                "fecha_fin": item["fecha_fin"],
                "activa": item["activa"],
            },
        )
        Sesion.objects.filter(pk=sesion.pk).update(fecha_inicio=item["fecha_inicio"])
        sesion.refresh_from_db()
        sesiones[item["codigo"]] = sesion

    return sesiones
