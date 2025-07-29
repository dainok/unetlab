"""UNetLab URL Configuration for the proxmox app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from template.views import (
    TemplateViewSet,
    TemplateListView,
    TemplateDetailView,
)

# DRF router for API endpoints of Template viewsets
router = DefaultRouter()
router.register(r"host", TemplateViewSet, basename="host")

# URL patterns for class-based views and API endpoints
urlpatterns = [
    # List and detail views for Template (HTML views)
    path("template/", TemplateListView.as_view(), name="template_list"),
    path("template/<int:pk>/", TemplateDetailView.as_view(), name="template_detail"),
    # Include API routes from DRF router
    path("api/", include(router.urls)),
]
