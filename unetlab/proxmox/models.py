"""Define ORM models for Proxmox hosts."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.db import models
from django.urls import reverse


class ProxmoxHost(models.Model):
    """
    Model for Proxmox host.

    The details of Proxmox hosts are retrieved and cached.
    """

    name = models.CharField(
        primary_key=True,
        max_length=256,
        null=False,
        blank=False,
        editable=False,
        help_text="Hostname retrived from Proxmox host.",
        verbose_name="Hostname",
    )
    ip_address = models.GenericIPAddressField(
        null=False,
        blank=False,
        default="0.0.0.0",  # nosec
        editable=False,
        help_text="IP address retrieved from Proxmox host.",
        verbose_name="IP Address",
    )
    is_online = models.BooleanField(
        default=False,
        editable=False,
        help_text="True if Proxmox host is reported as online.",
        verbose_name="Online",
    )  # True if the host is reported as online in the Proxmox cluster.
    is_orphan = models.BooleanField(
        default=True,
        editable=False,
        help_text="True if Proxmox host is not found in the Proxmox cluster.",
        verbose_name="Orphan",
    )  # True if the host does not exist in the Proxmox cluster.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        db_table = "hosts"
        ordering = ["name"]
        unique_together = ["name"]
        verbose_name = "Host"
        verbose_name_plural = "Hosts"

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.name

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("host-detail-view", args=[str(self.pk)])
