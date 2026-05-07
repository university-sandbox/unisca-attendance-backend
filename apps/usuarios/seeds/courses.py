from apps.cursos.models import Curso
from apps.usuarios.models import Docente
from apps.usuarios.seeds.data import CURSOS


def seed_courses():
    docentes = {
        docente.codigo_docente: docente
        for docente in Docente.objects.filter(
            codigo_docente__in=[item["codigo_docente"] for item in CURSOS]
        )
    }
    cursos = {}

    for item in CURSOS:
        curso, _ = Curso.objects.update_or_create(
            codigo=item["codigo"],
            defaults={
                "docente": docentes[item["codigo_docente"]],
                "nombre": item["nombre"],
                "ciclo_academico": item["ciclo_academico"],
            },
        )
        cursos[item["codigo"]] = curso

    return cursos
