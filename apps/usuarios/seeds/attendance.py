from apps.asistencias.models import Asistencia
from apps.usuarios.models import Estudiante
from apps.usuarios.seeds.data import ASISTENCIAS


def seed_attendance(sesiones):
    estudiantes = {
        estudiante.codigo_estudiante: estudiante
        for estudiante in Estudiante.objects.filter(
            codigo_estudiante__in=[item["codigo_estudiante"] for item in ASISTENCIAS]
        )
    }
    asistencias = []

    for item in ASISTENCIAS:
        asistencia, _ = Asistencia.objects.update_or_create(
            sesion=sesiones[item["sesion_codigo"]],
            estudiante=estudiantes[item["codigo_estudiante"]],
            defaults={
                "metodo": item["metodo"],
                "face_verified": item["face_verified"],
            },
        )
        Asistencia.objects.filter(pk=asistencia.pk).update(
            timestamp_registro=item["timestamp_registro"]
        )
        asistencia.refresh_from_db()
        asistencias.append(asistencia)

    return asistencias
