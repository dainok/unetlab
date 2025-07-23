"""UNetLab URL Configuration for the proxmox app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from proxmox.views import (
    ProxmoxHostViewSet,
    ProxmoxHostListView,
    ProxmoxHostDetailView,
)

# DRF router for API endpoints of ProxmoxHost viewsets
router = DefaultRouter()
router.register(r"host", ProxmoxHostViewSet, basename="host")

# URL patterns for class-based views and API endpoints
urlpatterns = [
    # List and detail views for ProxmoxHost (HTML views)
    path("host/", ProxmoxHostListView.as_view(), name="host_list"),
    path("host/<int:pk>/", ProxmoxHostDetailView.as_view(), name="host_detail"),
    # Include API routes from DRF router
    path("api/", include(router.urls)),
]
