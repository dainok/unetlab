"""UNetLab URL Configuration for the proxmox app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from node.views import (
    NodeTemplateAPIViewSet,
    NodeTemplateBulkDeleteView,
    NodeTemplateChangeView,
    NodeTemplateCreateView,
    NodeTemplateDeleteView,
    NodeTemplateDetailView,
    NodeTemplateListView,
)

# DRF router for API endpoints of Template viewsets
router = DefaultRouter()
router.register(r"template", NodeTemplateAPIViewSet, basename="template")

# URL patterns for class-based views and API endpoints
urlpatterns = [
    #########################################################################
    # Disk views (HTML)
    #########################################################################
    path(
        "template/<str:pk>/disk/create",
        NodeTemplateChangeView.as_view(),
        name="nodetemplate_disk_create",
    ),
    path(
        "template/<str:pk>/disk/<str:disk_checksum>/delete",
        NodeTemplateChangeView.as_view(),
        name="nodetemplate_disk_delete",
    ),
    #########################################################################
    # NodeTemplate views (HTML)
    #########################################################################
    path("template/", NodeTemplateListView.as_view(), name="nodetemplate_list"),
    path(
        "template/create", NodeTemplateCreateView.as_view(), name="nodetemplate_create"
    ),
    path(
        "template/delete",
        NodeTemplateBulkDeleteView.as_view(),
        name="nodetemplate_bulkdelete",
    ),
    path(
        "template/<str:pk>/delete",
        NodeTemplateDeleteView.as_view(),
        name="nodetemplate_delete",
    ),
    path(
        "template/<str:pk>/update",
        NodeTemplateChangeView.as_view(),
        name="nodetemplate_update",
    ),
    path(
        "template/<str:pk>/",
        NodeTemplateDetailView.as_view(),
        name="nodetemplate_detail",
    ),
    #########################################################################
    # Custom API endpoints
    #########################################################################
    # path(
    #     "api/template/<str:pk>/disk",
    #     DiskTemplateCreateAPIView.as_view(),
    #     name="disk-create",
    # ),
    #########################################################################
    # API endpoints
    #########################################################################
    path("api/", include(router.urls)),
]
