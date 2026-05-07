from django.test import TestCase

from apps.cursos.models import Curso, Sesion
from apps.usuarios.models import Docente, Usuario


class CursoSesionModelTests(TestCase):
    def setUp(self):
        usuario = Usuario.objects.create_user(
            username="docente1",
            password="password123",
            first_name="Ada",
            last_name="Lovelace",
            rol="docente",
        )
        self.docente = Docente.objects.create(
            usuario=usuario,
            codigo_docente="DOC-001",
            departamento="Ingenieria",
        )

    def test_curso_string_includes_code_and_name(self):
        curso = Curso.objects.create(
            docente=self.docente,
            nombre="Matematica Discreta",
            codigo="MAT-101",
            ciclo_academico=1,
        )

        self.assertEqual(str(curso), "MAT-101 - Matematica Discreta")

    def test_sesion_creates_unique_qr_token_and_starts_active(self):
        curso = Curso.objects.create(
            docente=self.docente,
            nombre="Matematica Discreta",
            codigo="MAT-101",
            ciclo_academico=1,
        )

        sesion = Sesion.objects.create(curso=curso)

        self.assertTrue(sesion.activa)
        self.assertIsNotNone(sesion.qr_token)

# Create your tests here.
