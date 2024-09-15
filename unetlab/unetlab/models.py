"""Models (ORM).

Define ORM models for UNetLab objects:
* A Host represents a Proxmox host.
* A Template represents a Proxmox template used in UNetLab.
* A Node represents a Proxmox virtual machine used in UNetLab.
* A Link represents a Proxmox virtual network used in UNetLab.
* A Lab represents an instance of a running lab.
* A Repository is a directory or a Git HTTPS URL used to retrieve Labs.
"""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.db import models
from django.urls import reverse


#
# Host model
#


class Host(models.Model):
    """
    Model for Host.

    The details of Proxmox hosts are retrieved and cached in this table.
    """

    address = models.CharField(primary_key=True, max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        db_table = "hosts"
        db_table_comment = "Proxmox hosts"
        ordering = ["address"]
        verbose_name = "Host"
        verbose_name_plural = "Hosts"

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.address

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("host-detail-view", args=[str(self.id)])


#
# Repository model
#


class Repository(models.Model):
    """
    Model for Repository.

    Store lab repository URIs and credentials.
    """

    name = models.CharField(primary_key=True, max_length=256)
    uri = models.CharField(max_length=256)
    username = models.CharField(max_length=256, null=True, blank=True)
    password = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        db_table = "repositories"
        db_table_comment = "Lab repositories"
        ordering = ["url"]
        verbose_name = "Repository"
        verbose_name_plural = "Repositories"

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.name

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("repository-detail-view", args=[str(self.id)])
