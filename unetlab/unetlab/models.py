"""Models (ORM).

Define ORM models for UNetLab objects:
* A Host represents a Proxmox host.
* A Lab represents an instance of a running lab.
* A Link represents a Proxmox virtual network used in UNetLab.
* A Node represents a Proxmox virtual machine used in UNetLab.
* A Repository is a directory or a Git HTTPS URL used to retrieve Labs.
* A Template represents a Proxmox template used in UNetLab.
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
# Lab model
#


class Lab(models.Model):
    """
    Model for Lab.

    Cache labs and store user instances.
    """

    author = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    parent = models.ForeignKey(
        to="self", on_delete=models.SET_NULL, editable=False, blank=True, null=True
    )
    repository = models.ForeignKey(
        to="Repository", on_delete=models.CASCADE, editable=False
    )
    uri = models.CharField(max_length=256, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        db_table = "lab"
        ordering = ["name"]
        verbose_name = "Lab"
        verbose_name_plural = "Labs"

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.uri

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("lab-detail-view", args=[str(self.id)])


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
        ordering = ["name"]
        verbose_name = "Repository"
        verbose_name_plural = "Repositories"

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.name

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("repository-detail-view", args=[str(self.id)])
