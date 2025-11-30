"""UNetLab URL Configuration."""

from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("", include("ui.urls")),
    # Include URLs from the local apps
    path("", include("job.urls")),
    path("", include("lab.urls")),
    path("", include("node.urls")),
    path("", include("proxmox.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
