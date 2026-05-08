from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.cursos.models import Curso, Sesion
from apps.usuarios.models import Docente, Estudiante, Usuario


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


class CursoSesionAPITests(APITestCase):
    def setUp(self):
        self.docente_usuario = Usuario.objects.create_user(
            username="docente1",
            password="password123",
            first_name="Ada",
            last_name="Lovelace",
            rol="docente",
        )
        self.docente = Docente.objects.create(
            usuario=self.docente_usuario,
            codigo_docente="DOC-001",
            departamento="Ingenieria",
        )
        self.otro_docente_usuario = Usuario.objects.create_user(
            username="docente2",
            password="password123",
            first_name="Alan",
            last_name="Turing",
            rol="docente",
        )
        self.otro_docente = Docente.objects.create(
            usuario=self.otro_docente_usuario,
            codigo_docente="DOC-002",
            departamento="Ciencias",
        )

    def test_docente_can_create_and_list_only_own_courses(self):
        Curso.objects.create(
            docente=self.otro_docente,
            nombre="Arquitectura",
            codigo="ARQ-101",
            ciclo_academico=1,
        )
        self.client.force_authenticate(user=self.docente_usuario)

        create_response = self.client.post(
            reverse("cursos-list"),
            {
                "nombre": "Matematica Discreta",
                "codigo": "MAT-101",
                "ciclo_academico": 1,
            },
            format="json",
        )
        list_response = self.client.get(reverse("cursos-list"))

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Curso.objects.get(codigo="MAT-101").docente, self.docente)
        self.assertEqual(len(list_response.data), 1)
        self.assertEqual(list_response.data[0]["codigo"], "MAT-101")

    def test_estudiante_cannot_access_course_management(self):
        estudiante_usuario = Usuario.objects.create_user(
            username="estudiante1",
            password="password123",
            rol="estudiante",
        )
        Estudiante.objects.create(
            usuario=estudiante_usuario,
            codigo_estudiante="EST-001",
            carrera="Sistemas",
            ciclo=5,
        )
        self.client.force_authenticate(user=estudiante_usuario)

        response = self.client.get(reverse("cursos-list"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_docente_can_create_session_for_owned_course_only(self):
        curso = Curso.objects.create(
            docente=self.docente,
            nombre="Matematica Discreta",
            codigo="MAT-101",
            ciclo_academico=1,
        )
        otro_curso = Curso.objects.create(
            docente=self.otro_docente,
            nombre="Arquitectura",
            codigo="ARQ-101",
            ciclo_academico=1,
        )
        self.client.force_authenticate(user=self.docente_usuario)

        own_response = self.client.post(
            reverse("sesiones-list"), {"curso": curso.id}, format="json"
        )
        other_response = self.client.post(
            reverse("sesiones-list"), {"curso": otro_curso.id}, format="json"
        )

        self.assertEqual(own_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(other_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Sesion.objects.filter(curso=curso).count(), 1)


# Create your tests here.
