"""Define ORM models for Proxmox hosts."""

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse
from repository.models import Repository
from ui.validators import AlphanumericValidator, VersionValidator, SimplePasswordalidator
from django.core.validators import DecimalValidator

class NodeTemplate(models.Model):
    """
    Model for Template.

    The details of Repository are retrieved and cached.
    """

    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name="templates",
        verbose_name=_("Repository"),
        help_text=_("Repository associated with this template."),
        editable=False,
    )
    name = models.CharField(
        max_length=255,
        editable=False,
        verbose_name=_("Name"),
        validators=[AlphanumericValidator],
        help_text=_("Template name."),
    )
    checksum = models.CharField(
        max_length=255, verbose_name=_("Checksum"), help_text=_("Template checksum."), editable=False,
    )
    os = models.CharField(
        max_length=255, verbose_name=_("OS"), help_text=_("Template Operating System."), 
        validators=[AlphanumericValidator],
    )
    vendor = models.CharField(
        max_length=255, verbose_name=_("Vendor"), help_text=_("Template vendor."),
        validators=[AlphanumericValidator],
    )
    version = models.CharField(
        max_length=255, verbose_name=_("Version"), help_text=_("Template version."),
        validators=[VersionValidator],

    )
    extra = models.CharField(
        max_length=255,
        default="",
        verbose_name=_("Extra"),
        help_text=_("Template label."),
        validators=[AlphanumericValidator],
    )
    cpu = models.IntegerField(
        default=1, verbose_name=_("CPU"), help_text=_("Minimum CPU required."),
    )
    ram = models.IntegerField(
        default=2, verbose_name=_("RAM"), help_text=_("Minimum GB of RAM required."),
    )
    nics = models.IntegerField(
        default=4,
        verbose_name=_("NIC"),
        help_text=_("Template default network interfaces."),
    )
    mgmt = models.IntegerField(
        default=0,
        verbose_name=_("Management interface"),
        help_text=_("Management interface, starting from 0."),
    )
    disks = models.JSONField(
        default=list,
        verbose_name=_("Disks"),
        help_text=_("List of URI to download disks."), editable=False
    )
    username = models.CharField(
        max_length=255, verbose_name=_("Username"), help_text=_("Username to login."),
        validators=[AlphanumericValidator],
    )
    password = models.CharField(
        max_length=255, verbose_name=_("Password"), help_text=_("Password to login."), validators=[SimplePasswordalidator]
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
