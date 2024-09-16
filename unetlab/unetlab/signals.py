"""
Django signals.

Intercept database operations and execute UNetLab functions.
"""

import os
import logging
from urllib.parse import urlparse
import yaml

from django.db.models.signals import post_save
from django.dispatch import receiver

from unetlab import models


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
                    lab, created = models.Lab.objects.get_or_create(
                        uri=lab_file, repository=instance, parent__isnull=True
                    )
                    if created:
                        # Update lab
                        lab.author = lab_data["metadata"]["author"]
                        lab.description = lab_data["metadata"]["description"]
                        lab.name = lab_data["metadata"]["name"]
                        lab.save()
    else:
        raise ValueError(f"{instance.name} has not a valid URI")
