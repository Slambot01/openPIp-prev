from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('proteins.urls')),  # All protein API endpoints under /api/
]
