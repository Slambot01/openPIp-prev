from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProteinViewSet, InteractionViewSet, UploadView

router = DefaultRouter()
router.register(r'proteins', ProteinViewSet)
router.register(r'interactions', InteractionViewSet, basename='interaction')

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', UploadView.as_view(), name='upload'),
]
