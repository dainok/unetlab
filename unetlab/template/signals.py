"""
Django signals module.

This module intercepts database events and triggers functions.
"""

from template.models import NodeTemplate
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=NodeTemplate)
def set_name(sender, instance, **kwargs):
    """Signal handler triggered before a Template instance is saved."""
    if instance.extra:
        instance.name = (
            f"{instance.vendor}-{instance.os}-{instance.version}-{instance.extra}"
        )
    else:
        instance.name = f"{instance.vendor}-{instance.os}-{instance.version}"
