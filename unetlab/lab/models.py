"""Define ORM models for Proxmox hosts."""

from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse
from node.models import Node
from ui.include.validators import (
    AlphanumericPhraseValidator,
)


#############################################################################
# Lab
#############################################################################


class Lab(models.Model):
    """
    Model for Lab.
    """

    name = models.CharField(
        max_length=255,
        editable=False,
        verbose_name=_("Name"),
        validators=[AlphanumericPhraseValidator],
        help_text=_("Template name."),
    )
    hld = models.JSONField(
        verbose_name=_("HLD"),
        help_text=_("High Level Design"),
    )
    lld = models.JSONField(
        verbose_name=_("LLD"),
        help_text=_("Low Level Design"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="labs")
    shared_groups = models.ManyToManyField(Group, related_name="labs", blank=True)
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


#############################################################################
# Instance
#############################################################################


class LabInstance(models.Model):
    """
    Model for lab instance.
    """

    lab = models.ForeignKey(
        Lab,
        on_delete=models.CASCADE,
        related_name="instances",
        blank=True,
    )
    lld = models.JSONField(
        verbose_name=_("LLD"),
        help_text=_("Low Level Design"),
    )
    nodes = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="instances")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="instances")
    shared_groups = models.ManyToManyField(Group, related_name="instances", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        db_table = "instances"
        ordering = ["created_at"]
        verbose_name = _("Instance")
        verbose_name_plural = _("Instances")

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return str(self.pk)

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("instance-detail-view", args=[str(self.pk)])
