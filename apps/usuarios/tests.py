from django.test import TestCase

from apps.usuarios.models import Docente, Estudiante, Usuario


class UsuarioProfileModelTests(TestCase):
    def test_docente_string_includes_name_and_code(self):
        usuario = Usuario.objects.create_user(
            username="docente1",
            password="password123",
            first_name="Ada",
            last_name="Lovelace",
            rol="docente",
        )
        docente = Docente.objects.create(
            usuario=usuario,
            codigo_docente="DOC-001",
            departamento="Ingenieria",
        )

        self.assertEqual(str(docente), "Ada Lovelace (DOC-001)")

    def test_estudiante_string_includes_name_and_code(self):
        usuario = Usuario.objects.create_user(
            username="estudiante1",
            password="password123",
            first_name="Grace",
            last_name="Hopper",
            rol="estudiante",
        )
        estudiante = Estudiante.objects.create(
            usuario=usuario,
            codigo_estudiante="EST-001",
            carrera="Sistemas",
            ciclo=5,
        )

        self.assertEqual(str(estudiante), "Grace Hopper (EST-001)")

# Create your tests here.
