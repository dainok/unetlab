"""Manage WebSocket messages."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

import json
from channels.generic.websocket import AsyncWebsocketConsumer
import django_rq

from unetlab.tasks import proxmox


class ActionConsumer(AsyncWebsocketConsumer):
    """Manage Actions coming from WebSockets users."""

    async def connect(self):
        """Accept a new WebSocket user."""
        # TODO: authentication is required before using WS
        self.user = self.scope["user"]
        print("*** CONNECT", self.user)

        # To avoid tracking of user's channel, add it to the well known group
        await self.channel_layer.group_add(
            f"group-{self.user}",
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        """Disconnect a WebSocket user."""
        print("*** DISCONNECT", self.user)

        # Remove user's channel from the well known group
        await self.channel_layer.group_discard(
            f"group-{self.user}",
            self.channel_name,
        )

    async def receive(self, text_data):
        """Receive a message from a WebSocket user."""
        print("*** RECEIVE", self.user)
        try:
            log = json.loads(text_data)
        except json.decoder.JSONDecodeError:
            print("NOT A LOG", text_data)
            return

        # TODO: validate the log schema
        print(log)

        # Forward action to Hosts via RQ
        queue = django_rq.get_queue("actions")
        queue.enqueue(proxmox.delete, node_id=32)
