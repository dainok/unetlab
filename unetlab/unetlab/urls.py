"""UNetLab URL Configuration."""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from unetlab import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.HomeView.as_view(), name="home"),
    # Authentication URLs
    path(
        "account/login",
        auth_views.LoginView.as_view(template_name="unetlab/login.html"),
        name="login",
    ),
    path(
        "account/logout",
        auth_views.LogoutView.as_view(template_name="unetlab/logout.html", next_page="login"),
        name="logout",
    ),
    # API token authentication
    path("api/token/", obtain_auth_token, name="api_token"),
    # Include URLs from the job app
    path("", include("job.urls")),
]
