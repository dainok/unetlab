"""UNetLab URL WebSocket Configuration (see asgi.py)."""

from django.urls import re_path
from unetlab import consumers

websocket_urlpatterns = [
    re_path(r"ws/log", consumers.LogConsumer.as_asgi()),
]
