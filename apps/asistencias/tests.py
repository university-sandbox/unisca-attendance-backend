from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

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


class AsistenciaAPITests(APITestCase):
    def setUp(self):
        docente_usuario = Usuario.objects.create_user(
            username="docente1",
            password="password123",
            first_name="Ada",
            last_name="Lovelace",
            rol="docente",
        )
        self.docente = Docente.objects.create(
            usuario=docente_usuario,
            codigo_docente="DOC-001",
            departamento="Ingenieria",
        )
        self.curso = Curso.objects.create(
            docente=self.docente,
            nombre="Matematica Discreta",
            codigo="MAT-101",
            ciclo_academico=1,
        )
        self.sesion = Sesion.objects.create(curso=self.curso)

        self.estudiante_usuario = Usuario.objects.create_user(
            username="estudiante1",
            password="password123",
            first_name="Grace",
            last_name="Hopper",
            rol="estudiante",
        )
        self.estudiante = Estudiante.objects.create(
            usuario=self.estudiante_usuario,
            codigo_estudiante="EST-001",
            carrera="Sistemas",
            ciclo=5,
        )

    def test_estudiante_registers_attendance_with_valid_qr_token(self):
        self.client.force_authenticate(user=self.estudiante_usuario)

        response = self.client.post(
            reverse("registrar-asistencia"),
            {"qr_token": str(self.sesion.qr_token), "face_verified": True},
            format="json",
        )

        asistencia = Asistencia.objects.get()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "registrado")
        self.assertEqual(response.data["metodo"], "qr+facial")
        self.assertEqual(asistencia.estudiante, self.estudiante)
        self.assertTrue(asistencia.face_verified)

    def test_duplicate_attendance_registration_is_rejected(self):
        Asistencia.objects.create(sesion=self.sesion, estudiante=self.estudiante)
        self.client.force_authenticate(user=self.estudiante_usuario)

        response = self.client.post(
            reverse("registrar-asistencia"),
            {"qr_token": str(self.sesion.qr_token), "face_verified": True},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Asistencia.objects.count(), 1)

    def test_inactive_session_token_is_rejected(self):
        self.sesion.activa = False
        self.sesion.save(update_fields=["activa"])
        self.client.force_authenticate(user=self.estudiante_usuario)

        response = self.client.post(
            reverse("registrar-asistencia"),
            {"qr_token": str(self.sesion.qr_token), "face_verified": True},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_face_verification_is_required_to_register_attendance(self):
        self.client.force_authenticate(user=self.estudiante_usuario)

        response = self.client.post(
            reverse("registrar-asistencia"),
            {"qr_token": str(self.sesion.qr_token), "face_verified": False},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Asistencia.objects.count(), 0)

    def test_missing_face_verification_is_rejected(self):
        self.client.force_authenticate(user=self.estudiante_usuario)

        response = self.client.post(
            reverse("registrar-asistencia"),
            {"qr_token": str(self.sesion.qr_token)},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Asistencia.objects.count(), 0)

    def test_docente_lists_attendance_for_owned_session(self):
        Asistencia.objects.create(
            sesion=self.sesion,
            estudiante=self.estudiante,
            metodo="qr",
        )
        self.client.force_authenticate(user=self.docente.usuario)

        response = self.client.get(
            reverse("listar-asistencia", kwargs={"sesion_id": self.sesion.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["estudiante_codigo"], "EST-001")

    def test_docente_cannot_list_attendance_for_another_docente_session(self):
        otro_docente_usuario = Usuario.objects.create_user(
            username="docente2",
            password="password123",
            rol="docente",
        )
        Docente.objects.create(
            usuario=otro_docente_usuario,
            codigo_docente="DOC-002",
            departamento="Ciencias",
        )
        self.client.force_authenticate(user=otro_docente_usuario)

        response = self.client.get(
            reverse("listar-asistencia", kwargs={"sesion_id": self.sesion.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


# Create your tests here.
