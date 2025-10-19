"""Define ORM models for Proxmox hosts."""

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from lab.models import LabInstance
from ui.include.validators import (
    AlphanumericValidator,
    VersionValidator,
    SimplePasswordValidator,
)
from proxmox.models import ProxmoxHost


class NodeTemplate(models.Model):
    """
    Model for Template.

    The details of Repository are retrieved and cached.
    """

    name = models.CharField(
        max_length=255,
        editable=False,
        verbose_name=_("Name"),
        validators=[AlphanumericValidator],
        help_text=_("Template name."),
    )
    os = models.CharField(
        max_length=255,
        verbose_name=_("OS"),
        help_text=_("Template Operating System."),
        validators=[AlphanumericValidator],
    )
    vendor = models.CharField(
        max_length=255,
        verbose_name=_("Vendor"),
        help_text=_("Template vendor."),
        validators=[AlphanumericValidator],
    )
    version = models.CharField(
        max_length=255,
        verbose_name=_("Version"),
        help_text=_("Template version."),
        validators=[VersionValidator],
    )
    extra = models.CharField(
        max_length=255,
        default="",
        verbose_name=_("Extra"),
        blank=True,
        help_text=_("Template label."),
        validators=[AlphanumericValidator],
    )
    cpu = models.IntegerField(
        default=1,
        verbose_name=_("CPU"),
        help_text=_("Minimum CPU required."),
    )
    ram = models.IntegerField(
        default=2,
        verbose_name=_("RAM"),
        help_text=_("Minimum GB of RAM required."),
    )
    nics = models.IntegerField(
        default=4,
        verbose_name=_("NIC"),
        help_text=_("Template default network interfaces."),
    )
    oob = models.BooleanField(
        default=True,
        verbose_name=_("OOB Management interface"),
        help_text=_("True if first interface is used for OOB management."),
    )
    disk_checksum = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name=_("Disk checksum"),
        help_text=_("MD5 hash."),
        editable=False,
    )
    username = models.CharField(
        max_length=255,
        verbose_name=_("Username"),
        help_text=_("Username to login."),
        validators=[AlphanumericValidator],
    )
    password = models.CharField(
        max_length=255,
        verbose_name=_("Password"),
        help_text=_("Password to login."),
        validators=[SimplePasswordValidator],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        db_table = "templates"
        ordering = ["vendor", "os", "version", "extra"]
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")
        unique_together = ["vendor", "os", "version", "extra"]

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.name

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("template-detail-view", args=[str(self.pk)])


class NodeGroup(models.Model):
    """
    Model for Group.
    """
    instance = models.ForeignKey(
        LabInstance,
        on_delete=models.CASCADE,
        related_name="node_groups",
        editable=False,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="node_groups", editable=False)

    class Meta:
        """Database metadata."""

        db_table = "groups"
        # ordering = ["name"]
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    # def __str__(self):
    #     """Return a human readable name when the object is printed."""
    #     return self.id

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("group-detail-view", args=[str(self.pk)])


class Network(models.Model):
    """
    Model for Network.
    """
    rid = models.IntegerField()
    instance = models.ForeignKey(
        LabInstance,
        on_delete=models.CASCADE,
        related_name="node_networks",
        editable=False,
    )
    running_description = models.CharField(
        max_length=255,
        editable=False,
        verbose_name=_("Name"),
        # validators=[AlphanumericValidator],
        help_text=_("Network name."),
    )
    # running_type=link["type"]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="node_networks", editable=False)

    class Meta:
        """Database metadata."""

        db_table = "networks"
        # ordering = ["name"]
        unique_together = [["user", "rid", "instance"]]
        verbose_name = _("Network")
        verbose_name_plural = _("Networks")

    # def __str__(self):
    #     """Return a human readable name when the object is printed."""
    #     return self.name

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("network-detail-view", args=[str(self.pk)])


class Node(models.Model):
    """
    Model for Node.
    """

    rid = models.IntegerField()
    instance = models.ForeignKey(
        LabInstance,
        on_delete=models.CASCADE,
        related_name="nodes",
        editable=False,
    )
    running_name = models.CharField(
        max_length=255,
        editable=False,
        verbose_name=_("Name"),
        validators=[AlphanumericValidator],
        help_text=_("Node name."),
    )
    proxmox_host = models.ForeignKey(
        ProxmoxHost,
        on_delete=models.CASCADE,
        related_name="nodes",
        verbose_name=_("Proxmox host"),
        help_text=_("Proxmox host associated with this node."),
        blank=True,
        null=True,
    )
    proxmox_id = models.IntegerField(
        verbose_name=_("Proxmox node ID"),
        help_text=_("Proxmox node ID associated with this node."),
        blank=True,
        null=True,
    )
    running_cpu = models.IntegerField(
        default=1,
        verbose_name=_("CPU"),
        help_text=_("Minimum CPU required."),
    )
    running_ram = models.IntegerField(
        default=2,
        verbose_name=_("RAM"),
        help_text=_("Minimum GB of RAM required."),
    )
    running_nics = models.IntegerField(
        default=4,
        verbose_name=_("NIC"),
        help_text=_("Template default network interfaces."),
    )
    template = models.ForeignKey(
        NodeTemplate,
        on_delete=models.CASCADE,
        related_name="nodes",
        verbose_name=_("Template"),
        help_text=_("Template associated with this node."),
        editable=False,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nodes", editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        db_table = "nodes"
        ordering = ["running_name"]
        unique_together = [["user", "rid", "instance"],]
        verbose_name = _("Node")
        verbose_name_plural = _("Nodes")

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.running_name

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("node-detail-view", args=[str(self.pk)])


class NodeInterface(models.Model):
    """
    Model for Interface.
    """
    rid = models.IntegerField()
    node = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name="node_interfaces",
        editable=False,
    )
    running_description = models.CharField(
        max_length=255,
        verbose_name=_("Description"),
        # validators=[AlphanumericValidator],
        help_text=_("Interface description."),
        blank=True,
        null=True,
    )
    link = models.ForeignKey(
        Network,
        on_delete=models.SET_NULL,
        related_name="node_interfaces",
        blank=True,
        null=True,
    )

    class Meta:
        """Database metadata."""

        db_table = "interfaces"
        ordering = ["id"]
        unique_together = [["node", "rid"]]
        verbose_name = _("Interface")
        verbose_name_plural = _("Interfaces")

    # def __str__(self):
    #     """Return a human readable name when the object is printed."""
    #     return self.id

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("interface-detail-view", args=[str(self.pk)])
