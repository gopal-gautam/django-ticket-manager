"""
URL configuration for config project.

Maps the root URL patterns to the tickets app API endpoints.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints (tickets, health check)
    path('api/', include('tickets.urls')),
]
