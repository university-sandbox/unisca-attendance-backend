from datetime import timedelta

from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
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

    def test_estudiante_face_diagnostic_is_recorded_in_server_logs(self):
        self.client.force_authenticate(user=self.estudiante_usuario)

        with self.assertLogs("apps.asistencias.views", level="INFO") as logs:
            response = self.client.post(
                reverse("face-verification-diagnostics"),
                {
                    "event": "verification_failed",
                    "stage": "loading_reference_image",
                    "client_origin": "https://app.example.com",
                    "reference_image_origin": "https://api.example.com",
                    "error_name": "TypeError",
                    "error_message": "Failed to fetch",
                },
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn("event=verification_failed", logs.output[0])
        self.assertIn("student_code=EST-001", logs.output[0])
        self.assertIn("stage=loading_reference_image", logs.output[0])

    def test_docente_cannot_report_face_diagnostics(self):
        self.client.force_authenticate(user=self.docente.usuario)

        response = self.client.post(
            reverse("face-verification-diagnostics"),
            {"event": "verification_started"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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

    def test_docente_lists_course_attendance_filtered_by_date(self):
        asistencia = Asistencia.objects.create(
            sesion=self.sesion,
            estudiante=self.estudiante,
            metodo="qr",
        )
        target_date = timezone.localdate() - timedelta(days=1)
        Asistencia.objects.filter(pk=asistencia.pk).update(
            timestamp_registro=timezone.now() - timedelta(days=1)
        )
        self.client.force_authenticate(user=self.docente.usuario)

        response = self.client.get(
            reverse("listar-asistencia-curso", kwargs={"curso_id": self.curso.id}),
            {"fecha": target_date.isoformat()},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["estudiante_codigo"], "EST-001")

    def test_course_attendance_returns_empty_page_without_records_for_date(self):
        Asistencia.objects.create(
            sesion=self.sesion,
            estudiante=self.estudiante,
            metodo="qr",
        )
        self.client.force_authenticate(user=self.docente.usuario)

        response = self.client.get(
            reverse("listar-asistencia-curso", kwargs={"curso_id": self.curso.id}),
            {"fecha": (timezone.localdate() - timedelta(days=3)).isoformat()},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])

    def test_course_attendance_is_paginated(self):
        for index in range(12):
            usuario = Usuario.objects.create_user(
                username=f"estudiante-page-{index}",
                password="password123",
                first_name="Student",
                last_name=f"{index:02d}",
                rol="estudiante",
            )
            estudiante = Estudiante.objects.create(
                usuario=usuario,
                codigo_estudiante=f"EST-P{index:03d}",
                carrera="Sistemas",
                ciclo=5,
            )
            sesion = Sesion.objects.create(curso=self.curso)
            Asistencia.objects.create(sesion=sesion, estudiante=estudiante)

        self.client.force_authenticate(user=self.docente.usuario)

        response = self.client.get(
            reverse("listar-asistencia-curso", kwargs={"curso_id": self.curso.id}),
            {"fecha": timezone.localdate().isoformat()},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 12)
        self.assertEqual(len(response.data["results"]), 10)


# Create your tests here.
