"""UNetLab URL Configuration."""

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
from unetlab import views

urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url="/static/unetlab/favicon.ico")),
    path("", views.HomeView.as_view(), name="home"),
    # Authentication URLs (standard users cannot use admin/login.html)
    path(
        "account/login",
        LoginView.as_view(template_name="admin/login.html"),
        name="login",
    ),
    path(
        "account/logout",
        LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    # API token authentication
    path("api/token/", obtain_auth_token, name="api_token"),
    # Include URLs from the local apps
    path("", include("job.urls")),
    path("", include("lab.urls")),
    path("", include("node.urls")),
    path("", include("proxmox.urls")),
    # path("", include("repository.urls")),
    path("", include("ui.urls")),
    # path("", include("ui.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
