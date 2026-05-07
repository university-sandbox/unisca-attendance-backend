from rest_framework.permissions import BasePermission


class IsEstudiante(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.rol == "estudiante"
            and hasattr(request.user, "estudiante")
        )


class IsDocente(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.rol == "docente"
            and hasattr(request.user, "docente")
        )
