"""URL configuration for Lab app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from lab.views import (
    # LabInstanceAPIViewSet,
    # LabInstanceBulkDeleteView,
    # # LabInstanceChangeView,
    # LabInstanceCreateView,
    # LabInstanceDeleteView,
    # LabInstanceDetailView,
    # LabInstanceListView,
    LabAPIViewSet,
    LabBulkDeleteView,
    LabChangeView,
    LabCreateView,
    LabDeleteView,
    LabDetailView,
    LabListView,
    # LabTopologyView,
)

# DRF router for API endpoints of Template viewsets
router = DefaultRouter()
router.register(r"lab", LabAPIViewSet, basename="lab")
# router.register(r"instance", LabInstanceAPIViewSet, basename="instance")

# URL patterns for class-based views and API endpoints
urlpatterns = [
    #########################################################################
    # Lab
    #########################################################################
    path("lab/", LabListView.as_view(), name="lab_list"),
    path("lab/create", LabCreateView.as_view(), name="lab_create"),
    path("lab/delete", LabBulkDeleteView.as_view(), name="lab_bulkdelete"),
    # path(
    #     "lab/<int:pk>/topology/<int:topology_id>",
    #     LabTopologyView.as_view(),
    #     name="lab_topology",
    # ),
    path("lab/<int:pk>/", LabDetailView.as_view(), name="lab_detail"),
    path("lab/<int:pk>/delete", LabDeleteView.as_view(), name="lab_delete"),
    path("lab/<int:pk>/update", LabChangeView.as_view(), name="lab_update"),
    #########################################################################
    # Instance
    #########################################################################
    # path("instance/", LabInstanceListView.as_view(), name="labinstance_list"),
    # path("instance/create", LabInstanceCreateView.as_view(), name="labinstance_create"),
    # path(
    #     "instance/delete",
    #     LabInstanceBulkDeleteView.as_view(),
    #     name="labinstance_bulkdelete",
    # ),
    # path(
    #     "instance/<int:pk>/delete",
    #     LabInstanceDeleteView.as_view(),
    #     name="labinstance_delete",
    # ),
    # # path(
    # #     "instance/<int:pk>/update",
    # #     LabInstanceChangeView.as_view(),
    # #     name="labinstance_update",
    # # ),
    # path(
    #     "instance/<int:pk>/", LabInstanceDetailView.as_view(), name="labinstance_detail"
    # ),
    #########################################################################
    # API endpoints
    #########################################################################
    path("api/", include(router.urls)),
]
