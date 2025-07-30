"""
Django signals module.

This module intercepts database events and triggers functions.
"""

from node.models import NodeTemplate
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=NodeTemplate)
def set_name(sender, instance, **kwargs):
    """Signal handler triggered before a Template instance is saved."""
    if instance.extra:
        instance.name = f"template-{instance.repository.name}-{instance.vendor}-{instance.os}-{instance.version}-{instance.extra}".lower()
    else:
        instance.name = f"template-{instance.repository.name}-{instance.vendor}-{instance.os}-{instance.version}".lower()
