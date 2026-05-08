from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

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


class UsuarioMeAPITests(APITestCase):
    def test_requires_authentication(self):
        response = self.client.get(reverse("usuario-me"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returns_authenticated_user_profile_with_photo_url(self):
        usuario = Usuario.objects.create_user(
            username="estudiante1",
            password="password123",
            first_name="Grace",
            last_name="Hopper",
            email="grace@example.com",
            rol="estudiante",
        )
        Estudiante.objects.create(
            usuario=usuario,
            codigo_estudiante="EST-001",
            carrera="Sistemas",
            ciclo=5,
            foto_perfil="fotos_perfil/grace.jpg",
        )
        self.client.force_authenticate(user=usuario)

        response = self.client.get(reverse("usuario-me"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "estudiante1")
        self.assertEqual(response.data["rol"], "estudiante")
        self.assertTrue(response.data["foto_perfil"].endswith("/media/fotos_perfil/grace.jpg"))

    def test_updates_allowed_profile_fields_only(self):
        usuario = Usuario.objects.create_user(
            username="docente1",
            password="password123",
            email="old@example.com",
            first_name="Ada",
            last_name="Lovelace",
            rol="docente",
        )
        self.client.force_authenticate(user=usuario)

        response = self.client.patch(
            reverse("usuario-me"),
            {
                "email": "ada@example.com",
                "first_name": "Augusta",
                "rol": "admin",
            },
            format="json",
        )

        usuario.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(usuario.email, "ada@example.com")
        self.assertEqual(usuario.first_name, "Augusta")
        self.assertEqual(usuario.rol, "docente")


# Create your tests here.
