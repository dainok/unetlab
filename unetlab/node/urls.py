"""UNetLab URL Configuration for the proxmox app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from node.views import (
    NodeTemplateViewSet,
    NodeTemplateListView,
    NodeTemplateDetailView,
)

# DRF router for API endpoints of Template viewsets
router = DefaultRouter()
router.register(r"template", NodeTemplateViewSet, basename="template")

# URL patterns for class-based views and API endpoints
urlpatterns = [
    # List and detail views for Template (HTML views)
    path("template/", NodeTemplateListView.as_view(), name="template_list"),
    path(
        "template/<int:pk>/", NodeTemplateDetailView.as_view(), name="template_detail"
    ),
    # Include API routes from DRF router
    path("api/", include(router.urls)),
]
