"""WebSocket URL routing configuration for UNetLab (used in asgi.py)."""

from django.urls import re_path
from unetlab import consumers

websocket_urlpatterns = [
    # Route WebSocket requests for actions to ActionConsumer
    re_path(r'ws/action', consumers.ActionConsumer.as_asgi()),
]
