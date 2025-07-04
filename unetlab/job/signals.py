"""
Django signals module.

This module intercepts database events (specifically model saves) and triggers
corresponding UNetLab functions such as broadcasting logs over WebSocket channels.
"""

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from job.models import Log
from django.db.models.signals import post_save
from django.dispatch import receiver
from job.serializers import LogSerializer


@receiver(post_save, sender=Log)
def post_save_log(sender, instance, created, **kwargs):
    """
    Signal handler triggered after a Log instance is saved.

    If the Log instance was newly created, serialize the log data and send it
    asynchronously to a Channels group for WebSocket broadcasting.

    Args:
        sender: The model class (Log).
        instance: The actual instance being saved.
        created: Boolean indicating if a new record was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        # Only send notifications for newly created Log entries.

        # Get the channel layer for sending messages via Channels.
        channel_layer = get_channel_layer()

        # TODO: Customize channel/group name based on the user or other context.
        channel = "broadcast"

        # Serialize the Log instance to JSON-compatible data.
        log = LogSerializer(instance)

        # Construct the event dict expected by Channels consumers.
        event = {
            "data": log.data,
            "type": "LOG",  # This type is used in unetlab.consumers to identify the message.
        }

        # Use async_to_sync to call async channel_layer.group_send from sync context.
        async_to_sync(channel_layer.group_send)(channel, event)
