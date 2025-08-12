"""UNetLab URL Configuration for the proxmox app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ui.views import (
    UserDetailView, UserListView, GroupDetailView, GroupListView, TokenDetailView, TokenListView,
    UserChangeView, UserCreateView, GroupChangeView, GroupCreateView
)

# DRF router for API endpoints of Template viewsets
router = DefaultRouter()
# router.register(r"group", GroupViewSet, basename="group")

# URL patterns for class-based views and API endpoints
urlpatterns = [
    # List and detail views for Template (HTML views)
    path("user/", UserListView.as_view(), name="user_list"),
    path("user/create", UserCreateView.as_view(), name="user_create"),
    path(
        "user/<str:pk>/update", UserChangeView.as_view(), name="user_update"
    ),
    path(
        "user/<int:pk>/", UserDetailView.as_view(), name="user_detail"
    ),
    path("group/", GroupListView.as_view(), name="group_list"),
    path("group/create", GroupCreateView.as_view(), name="group_create"),
    path(
        "group/<str:pk>/update", GroupChangeView.as_view(), name="group_update"
    ),
    path(
        "group/<int:pk>/", GroupDetailView.as_view(), name="group_detail"
    ),
    path("token/", TokenListView.as_view(), name="token_list"),
    # path("token/create", LabCreateView.as_view(), name="token_create"),
    # path(
    #     "token/<str:pk>/update", LabChangeView.as_view(), name="token_update"
    # ),
    path(
        "token/<int:pk>/", TokenDetailView.as_view(), name="token_detail"
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
