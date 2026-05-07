from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROL_CHOICES = [
        ("docente", "Docente"),
        ("estudiante", "Estudiante"),
        ("admin", "Admin"),
    ]

    rol = models.CharField(max_length=20, choices=ROL_CHOICES, blank=True)
