"""
Django signals module.

This module intercepts database events and triggers functions.
"""

from node.models import NodeTemplate
from repository.models import Repository
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


@receiver(pre_save, sender=NodeTemplate)
def set_repository(sender, instance, **kwargs):
    """Set name and local repository before Tempalte instance is saved."""
    if not instance.pk or not sender.objects.filter(pk=instance.pk).exists():
        # New instance
        # TODO: only local templates can be modified
        if not instance.repository_id:
            # Associate local repository
            local_repo, created = Repository.objects.get_or_create(name="local")
            if not local_repo.is_enabled:
                # Activate local repository
                local_repo.is_enabled = True
                local_repo.save()
            instance.repository_id = local_repo.pk

        repo = Repository.objects.get(pk=instance.repository_id)

        # Define repository name
        if instance.extra:
            instance.name = f"template-{repo.name}-{instance.vendor}-{instance.os}-{instance.version}-{instance.extra}".lower()
        else:
            instance.name = f"template-{repo.name}-{instance.vendor}-{instance.os}-{instance.version}".lower()

        instance.created_at = timezone.now()
        instance.updated_at = instance.created_at
