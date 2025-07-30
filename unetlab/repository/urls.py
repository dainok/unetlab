"""UNetLab URL Configuration for the proxmox app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from repository.views import (
    RepositoryViewSet,
    RepositoryListView,
    RepositoryDetailView,
    RepositoriesRescanView,
)

# DRF router for API endpoints of Repository viewsets
router = DefaultRouter()
router.register(r"host", RepositoryViewSet, basename="host")

# URL patterns for class-based views and API endpoints
urlpatterns = [
    # List and detail views for Repository (HTML views)
    path("repository/", RepositoryListView.as_view(), name="repository_list"),
    path(
        "repository/<str:pk>/", RepositoryDetailView.as_view(), name="repository_detail"
    ),
    # Custom API endpoints
    path(
        "api/repository/rescan/",
        RepositoriesRescanView.as_view(),
        name="repository-rescan",
    ),
    # Include API routes from DRF router
    path("api/", include(router.urls)),
]
