"""UNetLab URL Configuration for the proxmox app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from lab.views import (
    LabInstanceAPIViewSet,
    LabInstanceBulkDeleteView,
    LabInstanceChangeView,
    # LabInstanceCreateView,
    LabInstanceDeleteView,
    LabInstanceDetailView,
    LabInstanceListView,
    LabAPIViewSet,
    LabBulkDeleteView,
    LabChangeView,
    LabCreateView,
    LabDeleteView,
    LabDetailView,
    LabListView,
)

# DRF router for API endpoints of Template viewsets
router = DefaultRouter()
router.register(r"lab", LabAPIViewSet, basename="lab")
router.register(r"instance", LabInstanceAPIViewSet, basename="instance")

# URL patterns for class-based views and API endpoints
urlpatterns = [
    #########################################################################
    # Lab
    #########################################################################
    path("lab/", LabListView.as_view(), name="lab_list"),
    path("lab/create", LabCreateView.as_view(), name="lab_create"),
    path("lab/delete", LabBulkDeleteView.as_view(), name="lab_bulkdelete"),
    path("lab/<str:pk>/delete", LabDeleteView.as_view(), name="lab_delete"),
    path("lab/<str:pk>/update", LabChangeView.as_view(), name="lab_update"),
    path("lab/<str:pk>/", LabDetailView.as_view(), name="lab_detail"),
    #########################################################################
    # Instance
    #########################################################################
    path("instance/", LabInstanceListView.as_view(), name="labinstance_list"),
    # path("instance/create", LabCreateView.as_view(), name="labinstance_create"),
    path(
        "instance/delete",
        LabInstanceBulkDeleteView.as_view(),
        name="labinstance_bulkdelete",
    ),
    path(
        "instance/<str:pk>/delete",
        LabInstanceDeleteView.as_view(),
        name="labinstance_delete",
    ),
    path(
        "instance/<str:pk>/update",
        LabInstanceChangeView.as_view(),
        name="labinstance_update",
    ),
    path(
        "instance/<str:pk>/", LabInstanceDetailView.as_view(), name="labinstance_detail"
    ),
    #########################################################################
    # API endpoints
    #########################################################################
    path("api/", include(router.urls)),
]
