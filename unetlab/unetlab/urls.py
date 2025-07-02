"""UNetLab URL Configuration."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"


from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from unetlab import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.HomeView.as_view(), name="home"),
    path(
        "account/login",
        auth_views.LoginView.as_view(template_name="unetlab/login.html"),
        name="login",
    ),
    path(
        "account/logout",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    path("api/token/", obtain_auth_token, name="api_token"),
    path("", include("job.urls")),
]
