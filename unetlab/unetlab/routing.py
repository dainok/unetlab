"""UNetLab URL WebSocket Configuration (see asgi.py)."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.urls import re_path
from unetlab import consumers

websocket_urlpatterns = [
    re_path(r"ws/log", consumers.LogConsumer.as_asgi()),
]
