"""URL configuration for User, Group, and Token views.

This module defines both HTML views (class-based) and REST API endpoints
using Django REST Framework routers.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ui.views import (
    GroupAPIViewSet,
    GroupBulkDeleteView,
    GroupChangeView,
    GroupCreateView,
    GroupDeleteView,
    GroupDetailView,
    GroupListView,
    TokenDetailView,
    TokenListView,
    UserAPIViewSet,
    UserBulkDeleteView,
    UserChangeView,
    UserCreateView,
    UserDeleteView,
    UserDetailView,
    UserListView,
)

# DRF router for API endpoints
router = DefaultRouter()
router.register(r"group", GroupAPIViewSet, basename="group")
router.register(r"user", UserAPIViewSet, basename="user")

# URL patterns for class-based views and API endpoints
urlpatterns = [
    #########################################################################
    # Group views (HTML)
    #########################################################################
    path("group/", GroupListView.as_view(), name="group_list"),
    path("group/create", GroupCreateView.as_view(), name="group_create"),
    path("group/delete", GroupBulkDeleteView.as_view(), name="group_bulkdelete"),
    path("group/<int:pk>/delete/", GroupDeleteView.as_view(), name="group_delete"),
    path("group/<int:pk>/update", GroupChangeView.as_view(), name="group_update"),
    path("group/<int:pk>/", GroupDetailView.as_view(), name="group_detail"),
    #########################################################################
    # User views (HTML)
    #########################################################################
    path("user/", UserListView.as_view(), name="user_list"),
    path("user/create", UserCreateView.as_view(), name="user_create"),
    path("user/delete", UserBulkDeleteView.as_view(), name="user_bulkdelete"),
    path("user/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),
    path("user/<int:pk>/update", UserChangeView.as_view(), name="user_update"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    #########################################################################
    # Token views (HTML)
    #########################################################################
    # path("token/", TokenListView.as_view(), name="token_list"),
    # path("token/create", LabCreateView.as_view(), name="token_create"),
    # path(
    #     "token/<str:pk>/update", LabChangeView.as_view(), name="token_update"
    # ),
    # path("token/<int:pk>/", TokenDetailView.as_view(), name="token_detail"),
    #########################################################################
    # API endpoints
    #########################################################################
    path("api/", include(router.urls)),
]
