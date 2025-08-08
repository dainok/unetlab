"""UNetLab URL Configuration for the proxmox app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from node.views import (
    NodeTemplateViewSet,
    NodeTemplateListView,
    NodeTemplateDetailView,
    NodeTemplateChangeView,
    NodeTemplateCreateView,
)

# DRF router for API endpoints of Template viewsets
router = DefaultRouter()
router.register(r"template", NodeTemplateViewSet, basename="template")

# URL patterns for class-based views and API endpoints
urlpatterns = [
    # List and detail views for Template (HTML views)
    path("template/", NodeTemplateListView.as_view(), name="template_list"),
    path("template/create", NodeTemplateCreateView.as_view(), name="template_create"),
    path(
        "template/<str:pk>/update", NodeTemplateChangeView.as_view(), name="template_update"
    ),
    path(
        "template/<str:pk>/", NodeTemplateDetailView.as_view(), name="template_detail"
    ),
    # Include API routes from DRF router
    path("api/", include(router.urls)),
]
