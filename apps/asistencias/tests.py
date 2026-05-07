from django.db import IntegrityError
from django.test import TestCase

from apps.asistencias.models import Asistencia
from apps.cursos.models import Curso, Sesion
from apps.usuarios.models import Docente, Estudiante, Usuario


class AsistenciaModelTests(TestCase):
    def setUp(self):
        docente_usuario = Usuario.objects.create_user(
            username="docente1",
            password="password123",
            first_name="Ada",
            last_name="Lovelace",
            rol="docente",
        )
        docente = Docente.objects.create(
            usuario=docente_usuario,
            codigo_docente="DOC-001",
            departamento="Ingenieria",
        )
        curso = Curso.objects.create(
            docente=docente,
            nombre="Matematica Discreta",
            codigo="MAT-101",
            ciclo_academico=1,
        )
        self.sesion = Sesion.objects.create(curso=curso)

        estudiante_usuario = Usuario.objects.create_user(
            username="estudiante1",
            password="password123",
            first_name="Grace",
            last_name="Hopper",
            rol="estudiante",
        )
        self.estudiante = Estudiante.objects.create(
            usuario=estudiante_usuario,
            codigo_estudiante="EST-001",
            carrera="Sistemas",
            ciclo=5,
        )

    def test_asistencia_is_unique_per_session_and_student(self):
        Asistencia.objects.create(sesion=self.sesion, estudiante=self.estudiante)

        with self.assertRaises(IntegrityError):
            Asistencia.objects.create(sesion=self.sesion, estudiante=self.estudiante)

# Create your tests here.
