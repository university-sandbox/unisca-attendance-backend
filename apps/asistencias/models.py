from django.db import models

from apps.cursos.models import Sesion
from apps.usuarios.models import Estudiante


class Asistencia(models.Model):
    METODO_CHOICES = [
        ("qr", "Solo QR"),
        ("facial", "Solo Facial"),
        ("qr+facial", "QR + Facial"),
    ]

    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE, related_name="asistencias")
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    timestamp_registro = models.DateTimeField(auto_now_add=True)
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES, default="qr+facial")
    face_verified = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sesion", "estudiante"], name="unique_asistencia_por_sesion"
            )
        ]

    def __str__(self):
        return f"{self.estudiante} -> Sesion {self.sesion_id} [{self.metodo}]"
