"""Define ORM models for Proxmox hosts."""

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse


class Template(models.Model):
    """
    Model for Template.

    The details of Repository are retrieved and cached.
    """

    name = models.CharField(primary_key=True, max_length=255, editable=False)
    checksum = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    extra = models.CharField(max_length=255, default="")
    cpu = models.IntegerField(default=1)
    ram = models.IntegerField(default=2)
    nics = models.IntegerField(default=4)
    mgmt = models.IntegerField(default=0)
    disks = models.JSONField(default=[])
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        """Database metadata."""

        db_table = "templates"
        ordering = ["vendor", "os", "version", "extra"]
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.name

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("template-detail-view", args=[str(self.pk)])
