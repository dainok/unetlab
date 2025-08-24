"""UNetLab URL Configuration for the proxmox app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from proxmox.views import (
    ProxmoxHostAPIViewSet,
    ProxmoxHostListView,
    ProxmoxHostDetailView,
)

# DRF router for API endpoints of ProxmoxHost viewsets
router = DefaultRouter()
router.register(r"host", ProxmoxHostAPIViewSet, basename="host")

# URL patterns for class-based views and API endpoints
urlpatterns = [
    path("host/", ProxmoxHostListView.as_view(), name="host_list"),
    path("host/<str:pk>/", ProxmoxHostDetailView.as_view(), name="host_detail"),
    #########################################################################
    # API endpoints
    #########################################################################
    path("api/", include(router.urls)),
]
