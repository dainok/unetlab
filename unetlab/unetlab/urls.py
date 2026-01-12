"""UNetLab URL Configuration."""

from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('ui.urls')),
    # Include URLs from the local apps
    # path("", include("job.urls")),
    path('', include('lab.urls')),
    # path("", include("node.urls")),
    # path("", include("proxmox.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
