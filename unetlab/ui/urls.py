"""URL configuration for UI app."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from ui.views import ConstanceListView, ConstanceUpdateView
from ui.views import (
    GroupAPIViewSet,
    GroupBulkDeleteView,
    GroupChangeView,
    GroupCreateView,
    GroupDeleteView,
    GroupDetailView,
    GroupListView,
    HomeView,
    TokenBulkDeleteView,
    TokenCreateView,
    TokenDeleteView,
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
    path("favicon.ico", RedirectView.as_view(url="/static/ui/favicon.ico")),
    path("", HomeView.as_view(), name="home"),
    #########################################################################
    # Authentication URLs (standard users cannot use admin/login.html)
    #########################################################################
    path(
        "accounts/login/",
        LoginView.as_view(template_name="admin/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    #########################################################################
    # Contance settings (HTML)
    #########################################################################
    path("settings/", ConstanceListView.as_view(), name="settings_list"),
    path("settings/edit", ConstanceUpdateView.as_view(), name="settings_update"),
    #########################################################################
    # Group views (HTML)
    #########################################################################
    path("group/", GroupListView.as_view(), name="group_list"),
    path("group/create", GroupCreateView.as_view(), name="group_create"),
    path("group/delete", GroupBulkDeleteView.as_view(), name="group_bulkdelete"),
    path("group/<int:pk>/", GroupDetailView.as_view(), name="group_detail"),
    path("group/<int:pk>/delete", GroupDeleteView.as_view(), name="group_delete"),
    path("group/<int:pk>/update", GroupChangeView.as_view(), name="group_update"),
    #########################################################################
    # User views (HTML)
    #########################################################################
    path("user/", UserListView.as_view(), name="user_list"),
    path("user/create", UserCreateView.as_view(), name="user_create"),
    path("user/delete", UserBulkDeleteView.as_view(), name="user_bulkdelete"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("user/<int:pk>/delete", UserDeleteView.as_view(), name="user_delete"),
    path("user/<int:pk>/update", UserChangeView.as_view(), name="user_update"),
    #########################################################################
    # Token views (HTML)
    #########################################################################
    path("token/", TokenListView.as_view(), name="token_list"),
    path("token/create", TokenCreateView.as_view(), name="token_create"),
    path("token/delete", TokenBulkDeleteView.as_view(), name="token_bulkdelete"),
    path("token/<str:pk>/delete", TokenDeleteView.as_view(), name="token_delete"),
    #########################################################################
    # API endpoints
    #########################################################################
    path("api/", include(router.urls)),
    path("api/token/", obtain_auth_token, name="api_token"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
