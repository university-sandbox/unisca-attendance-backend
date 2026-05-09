from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.usuarios.models import Docente, Estudiante, Usuario


def fake_image(name="profile.gif"):
    return SimpleUploadedFile(
        name,
        b"GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;",
        content_type="image/gif",
    )


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
        self.assertEqual(response.data["codigo_estudiante"], "EST-001")
        self.assertEqual(response.data["carrera"], "Sistemas")
        self.assertEqual(response.data["ciclo"], 5)

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

    def test_updates_role_profile_fields_but_keeps_unique_fields_locked(self):
        usuario = Usuario.objects.create_user(
            username="estudiante1",
            password="password123",
            first_name="Grace",
            last_name="Hopper",
            email="grace@example.com",
            rol="estudiante",
        )
        estudiante = Estudiante.objects.create(
            usuario=usuario,
            codigo_estudiante="EST-001",
            carrera="Sistemas",
            ciclo=5,
        )
        self.client.force_authenticate(user=usuario)

        response = self.client.patch(
            reverse("usuario-me"),
            {
                "first_name": "Grace B.",
                "codigo_estudiante": "EST-999",
                "carrera": "Ingenieria de Software",
                "ciclo": 6,
            },
            format="json",
        )

        usuario.refresh_from_db()
        estudiante.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(usuario.first_name, "Grace B.")
        self.assertEqual(estudiante.codigo_estudiante, "EST-001")
        self.assertEqual(estudiante.carrera, "Ingenieria de Software")
        self.assertEqual(estudiante.ciclo, 6)

    def test_student_can_upload_profile_photo_for_first_time(self):
        usuario = Usuario.objects.create_user(
            username="estudiante1",
            password="password123",
            rol="estudiante",
        )
        estudiante = Estudiante.objects.create(
            usuario=usuario,
            codigo_estudiante="EST-001",
            carrera="Sistemas",
            ciclo=5,
        )
        self.client.force_authenticate(user=usuario)

        response = self.client.patch(
            reverse("usuario-me"),
            {"foto_perfil_upload": fake_image()},
            format="multipart",
        )

        estudiante.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(estudiante.foto_perfil)
        self.assertIsNotNone(estudiante.foto_perfil_updated_at)

    def test_student_cannot_upload_profile_photo_before_five_months(self):
        usuario = Usuario.objects.create_user(
            username="estudiante1",
            password="password123",
            rol="estudiante",
        )
        previous_update = timezone.now() - timedelta(days=30)
        estudiante = Estudiante.objects.create(
            usuario=usuario,
            codigo_estudiante="EST-001",
            carrera="Sistemas",
            ciclo=5,
            foto_perfil="fotos_perfil/current.jpg",
            foto_perfil_updated_at=previous_update,
        )
        self.client.force_authenticate(user=usuario)

        response = self.client.patch(
            reverse("usuario-me"),
            {"foto_perfil_upload": fake_image("new.gif")},
            format="multipart",
        )

        estudiante.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(estudiante.foto_perfil.name, "fotos_perfil/current.jpg")
        self.assertEqual(estudiante.foto_perfil_updated_at, previous_update)

    def test_student_can_upload_profile_photo_after_five_months(self):
        usuario = Usuario.objects.create_user(
            username="estudiante1",
            password="password123",
            rol="estudiante",
        )
        estudiante = Estudiante.objects.create(
            usuario=usuario,
            codigo_estudiante="EST-001",
            carrera="Sistemas",
            ciclo=5,
            foto_perfil="fotos_perfil/current.jpg",
            foto_perfil_updated_at=timezone.now() - timedelta(days=160),
        )
        self.client.force_authenticate(user=usuario)

        response = self.client.patch(
            reverse("usuario-me"),
            {"foto_perfil_upload": fake_image("new.gif")},
            format="multipart",
        )

        estudiante.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("new", estudiante.foto_perfil.name)


# Create your tests here.
