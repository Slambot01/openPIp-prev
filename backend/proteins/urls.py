from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProteinViewSet

router = DefaultRouter()
router.register(r'proteins', ProteinViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
