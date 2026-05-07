import uuid

from django.db import models

from apps.usuarios.models import Docente


class Curso(models.Model):
    docente = models.ForeignKey(
        Docente, on_delete=models.CASCADE, related_name="cursos"
    )
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=20, unique=True)
    ciclo_academico = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Sesion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="sesiones")
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    qr_token = models.UUIDField(default=uuid.uuid4, unique=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"Sesion {self.id} - {self.curso.codigo}"
