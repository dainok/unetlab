"""Define ORM models for Lab app."""

from django.db import models, transaction
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from lab.validators import HLDValidator
from ui.include.validators import (
    PhraseValidator,
    YAMLValidator,
)


#############################################################################
# Lab
#############################################################################


class Lab(models.Model):
    """
    Model for lab.
    """

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        validators=[PhraseValidator],
        help_text=_("Lab name."),
        unique=True,
        db_index=True,
    )
    hld = models.JSONField(
        verbose_name=_("HLD"),
        help_text=_("High Level Description"),
        validators=[HLDValidator],
        default=dict,
        blank=True,
    )
    lld = models.JSONField(
        verbose_name=_("LLD"),
        help_text=_("Low Level Description"),
        validators=[YAMLValidator],
        default=dict,
        editable=False,
        blank=True,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="labs", editable=False
    )
    shared_group = models.ForeignKey(
        Group,
        related_name="labs",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        db_table = "labs"
        ordering = ["name"]
        verbose_name = _("Lab")
        verbose_name_plural = _("Labs")

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.name

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("lab-detail-view", args=[str(self.pk)])

    def save(self, *args, **kwargs):
        # Force validators
        self.full_clean()
        super().save(*args, **kwargs)


#############################################################################
# Instance
#############################################################################


# class LabInstance(models.Model):
#     """
#     Model for lab instance.
#     """

#     lab = models.ForeignKey(
#         Lab,
#         on_delete=models.CASCADE,
#         related_name="instances",
#         editable=False,
#     )
#     instance_id = models.PositiveIntegerField(editable=False)
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="instances", editable=False
#     )
#     shared_groups = models.ManyToManyField(Group, related_name="instances", blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


#     class Meta:
#         """Database metadata."""

#         db_table = "instances"
#         ordering = ["-updated_at"]
#         unique_together = ["instance_id", "lab", "user"]
#         verbose_name = _("Instance")
#         verbose_name_plural = _("Instances")

#     def __str__(self):
#         """Return a human readable name when the object is printed."""
#         return f"{self.lab.name} ({self.instance_id})"

#     def get_absolute_url(self):
#         """Return the absolute url."""
#         return reverse("instance-detail-view", args=[str(self.pk)])

#     def save(self, *args, **kwargs):
#         if not self.pk:
#             # New object
#             with transaction.atomic():
#                 # Get highest instance ID for the same lab
#                 last_instance_id = LabInstance.objects.filter(
#                     user=self.user, lab=self.lab
#                 ).aggregate(models.Max("instance_id"))["instance_id__max"]
#                 # Generate a new isntance ID for the same lab
#                 self.instance_id = (last_instance_id or 0) + 1
#         super().save(*args, **kwargs)
