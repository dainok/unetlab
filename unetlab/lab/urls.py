"""UNetLab URL Configuration for the proxmox app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from lab.views import (
    LabViewSet,
    LabListView,
    LabDetailView,
    LabChangeView,
    LabCreateView,
    DiskTemplateCreateAPIView,
)

# DRF router for API endpoints of Template viewsets
router = DefaultRouter()
router.register(r"lab", LabViewSet, basename="lab")

# URL patterns for class-based views and API endpoints
urlpatterns = [
    # List and detail views for Template (HTML views)
    path("lab/", LabListView.as_view(), name="lab_list"),
    path("lab/create", LabCreateView.as_view(), name="lab_create"),
    path(
        "lab/<str:pk>/update", LabChangeView.as_view(), name="lab_update"
    ),
    path(
        "lab/<str:pk>/", LabDetailView.as_view(), name="lab_detail"
    ),
    # Custom API endpoints
    # path(
    #     "api/lab/<str:pk>/disk",
    #     DiskTemplateCreateAPIView.as_view(),
    #     name="disk-create",
    # ),
    # Include API routes from DRF router
    path("api/", include(router.urls)),
]
