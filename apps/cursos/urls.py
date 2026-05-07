from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.cursos.views import CursoViewSet, SesionViewSet

router = DefaultRouter()
router.register("cursos", CursoViewSet, basename="cursos")
router.register("sesiones", SesionViewSet, basename="sesiones")

urlpatterns = [
    path("", include(router.urls)),
]
