"""UNetLab URL Configuration."""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from unetlab import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.HomeView.as_view(), name="home"),
    # API token authentication
    path("api/token/", obtain_auth_token, name="api_token"),
    # Include URLs from the local apps
    path("", include("job.urls")),
    # path("", include("ui.urls")),
]
