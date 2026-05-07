from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROL_CHOICES = [
        ("docente", "Docente"),
        ("estudiante", "Estudiante"),
        ("admin", "Admin"),
    ]

    rol = models.CharField(max_length=20, choices=ROL_CHOICES)


class Docente(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="docente"
    )
    codigo_docente = models.CharField(max_length=20, unique=True)
    departamento = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.usuario.get_full_name()} ({self.codigo_docente})"


class Estudiante(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="estudiante"
    )
    codigo_estudiante = models.CharField(max_length=20, unique=True)
    carrera = models.CharField(max_length=100)
    ciclo = models.PositiveIntegerField()
    foto_perfil = models.ImageField(upload_to="fotos_perfil/", null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.get_full_name()} ({self.codigo_estudiante})"
