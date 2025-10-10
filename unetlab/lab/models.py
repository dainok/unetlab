"""Define ORM models for Proxmox hosts."""

from django.db import models, transaction
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
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
        verbose_name=_("Name"),
        validators=[AlphanumericPhraseValidator],
        help_text=_("Template name."),
        unique=True,
        db_index=True,
    )
    hld = models.JSONField(
        verbose_name=_("HLD"),
        help_text=_("High Level Description"),
        default=dict,
        blank=True,
    )
    lld = models.JSONField(
        verbose_name=_("LLD"),
        help_text=_("Low Level Description"),
        default=dict,
        editable=False,
        blank=True,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="labs", editable=False
    )
    shared_group = models.ForeignKey(
        Group, related_name="labs", on_delete=models.SET_NULL, blank=True, null=True
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
        editable=False,
    )
    rid = models.PositiveIntegerField(editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="instances", editable=False)
    shared_groups = models.ManyToManyField(Group, related_name="instances", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        db_table = "instances"
        ordering = ["-updated_at"]
        unique_together = ["rid", "lab", "user"]
        verbose_name = _("Instance")
        verbose_name_plural = _("Instances")

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return str(self.pk)

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("instance-detail-view", args=[str(self.pk)])

    def save(self, *args, **kwargs):
        if not self.rid:
            with transaction.atomic():
                self.running_name = self.lab.name
                last_rid = LabInstance.objects.filter(user=self.user, lab=self.lab).aggregate(models.Max("rid"))["rid__max"]
                self.rid = (last_rid or 0) + 1
        super().save(*args, **kwargs)