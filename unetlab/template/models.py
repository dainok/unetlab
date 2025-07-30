"""Define ORM models for Proxmox hosts."""

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse


class NodeTemplate(models.Model):
    """
    Model for Template.

    The details of Repository are retrieved and cached.
    """

    name = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
        verbose_name=_("Name"),
        help_text=_("Template name."),
    )
    checksum = models.CharField(
        max_length=255, verbose_name=_("Checksum"), help_text=_("Template checksum.")
    )
    os = models.CharField(
        max_length=255, verbose_name=_("OS"), help_text=_("Template Operating System.")
    )
    vendor = models.CharField(
        max_length=255, verbose_name=_("Vendor"), help_text=_("Template vendor.")
    )
    version = models.CharField(
        max_length=255, verbose_name=_("Version"), help_text=_("Template version.")
    )
    extra = models.CharField(
        max_length=255,
        default="",
        verbose_name=_("Extra"),
        help_text=_("Template label."),
    )
    cpu = models.IntegerField(
        default=1, verbose_name=_("CPU"), help_text=_("Minimum CPU required.")
    )
    ram = models.IntegerField(
        default=2, verbose_name=_("RAM"), help_text=_("Minimum GB of RAM required.")
    )
    nics = models.IntegerField(
        default=4,
        verbose_name=_("NIC"),
        help_text=_("Template default network interfaces."),
    )
    mgmt = models.IntegerField(
        default=0,
        verbose_name=_("Management ID"),
        help_text=_("Management interface, starting from 0."),
    )
    disks = models.JSONField(
        default=list,
        verbose_name=_("Disks"),
        help_text=_("List of URI to download disks."),
    )
    username = models.CharField(
        max_length=255, verbose_name=_("Username"), help_text=_("Username to login.")
    )
    password = models.CharField(
        max_length=255, verbose_name=_("Password"), help_text=_("Password to login.")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
