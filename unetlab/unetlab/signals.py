"""
Django signals.

Intercept database operations and execute UNetLab functions.
"""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

import os
import logging
from urllib.parse import urlparse
import yaml
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.db.models.signals import post_save
from django.dispatch import receiver

from unetlab import models


@receiver(post_save, sender=models.Log)
def post_save_log(sender, instance, created, **kwargs):
    """Send log to channels."""
    if created:
        # Send only new Logs
        channel_layer = get_channel_layer()

        # TODO: channel depends on the user
        channel = "broadcast"

        log = {
            "source": instance.source,
            "type": instance.type,
            "user": instance.user,
            "severity": instance.severity,
            "message": instance.message,
        }
        async_to_sync(channel_layer.group_send)(channel, log)


@receiver(post_save, sender=models.Repository)
def post_save_repository(sender, instance, **kwargs):
    """Scan labs and update Lab table."""
    uri = urlparse(instance.uri)
    if uri.scheme == "file":
        # Find lab files
        for dirpath, dirnames, filenames in os.walk(uri.path):
            for filename in filenames:
                if filename.endswith(".yml"):
                    # Load lab data from YAML file
                    lab_file = f"{dirpath}/{filename}"
                    with open(lab_file, "r") as fh:
                        try:
                            lab_data = yaml.safe_load(fh)
                        except yaml.YAMLError as exc:
                            logging.error(f"Invalid lab on file {lab_file}")
                            logging.debug(exc)

                    # Validate lab against schema (TODO)

                    # Get or create lab
                    lab_obj, created = models.Lab.objects.get_or_create(
                        uri=lab_file, repository=instance, parent__isnull=True
                    )
                    if created:
                        # Update lab
                        lab_obj.author = lab_data["metadata"]["author"]
                        lab_obj.description = lab_data["metadata"]["description"]
                        lab_obj.name = lab_data["metadata"]["name"]
                        lab_obj.save()
    else:
        raise ValueError(f"{instance.name} has not a valid URI")
