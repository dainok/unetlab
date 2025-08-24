"""UNetLab URL Configuration for the proxmox app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from repository.views import (
    RepositoryAPIViewSet,
    RepositoryBulkDeleteView,
    RepositoryCreateView,
    RepositoryDeleteView,
    RepositoryDetailView,
    RepositoryListView,
    RepositoryChangeView,
)

# DRF router for API endpoints of Repository viewsets
router = DefaultRouter()
router.register(r"repository", RepositoryAPIViewSet, basename="repository")

# URL patterns for class-based views and API endpoints
urlpatterns = [
    path("repository/", RepositoryListView.as_view(), name="repository_list"),
    path("repository/create", RepositoryCreateView.as_view(), name="repository_create"),
    path(
        "repository/delete",
        RepositoryBulkDeleteView.as_view(),
        name="repository_bulkdelete",
    ),
    path(
        "repository/<str:pk>/delete",
        RepositoryDeleteView.as_view(),
        name="repository_delete",
    ),
    path(
        "repository/<str:pk>/update",
        RepositoryChangeView.as_view(),
        name="repository_update",
    ),
    path(
        "repository/<str:pk>/", RepositoryDetailView.as_view(), name="repository_detail"
    ),
    #########################################################################
    # API endpoints
    #########################################################################
    path("api/", include(router.urls)),
]
