"""Define ORM models for Node app."""

# from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# from lab.models import LabInstance

# from proxmox.models import ProxmoxHost

# NODETEMPLATE_TYPE_CHOICES = [
#     ("docker", "Docker"),
#     ("qemu", "QEMU"),
# ]

#############################################################################
# Node Template
#############################################################################


class NodeTemplate(models.Model):
    """
    Model for NodeTemplate.

    The details of Repository are retrieved and cached.
    """

    path = models.CharField(
        unique=True,
        help_text='Directory of the template.',
    )
    template = models.JSONField(help_text='Template configuration.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        db_table = 'templates'
        ordering = ['path']
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.path

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse('template-detail-view', args=[str(self.pk)])


#############################################################################
# Disk Template
#############################################################################


# class DiskTemplate(models.Model):
#     filename = models.CharField(primary_key=True, editable=False)
#     checksum = models.CharField(
#         max_length=64,
#         default=None,
#         null=True,
#         blank=True,
#         verbose_name=_('Checksum'),
#         help_text=_('MD5 hash.'),
#         editable=False,
#     )
#     order = models.IntegerField(
#         default=0,
#         verbose_name=_('Order'),
#         help_text=_('Disk order, starting from 0.'),
#     )
#     template = models.ForeignKey(
#         NodeTemplate,
#         on_delete=models.CASCADE,
#         related_name='disks',
#         editable=False,
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         """Database metadata."""

#         db_table = 'disks'
#         ordering = ['filename']
#         verbose_name = _('Disk')
#         verbose_name_plural = _('Disks')

#     def __str__(self):
#         """Return a human readable name when the object is printed."""
#         return self.filename

#     def get_absolute_url(self):
#         """Return the absolute url."""
#         return reverse('disk-detail-view', args=[str(self.pk)])


# class NodeGroup(models.Model):
#     """
#     Model for Group.
#     """

#     instance = models.ForeignKey(
#         LabInstance,
#         on_delete=models.CASCADE,
#         related_name="node_groups",
#         editable=False,
#     )
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="node_groups", editable=False
#     )

#     class Meta:
#         """Database metadata."""

#         db_table = "groups"
#         # ordering = ["name"]
#         verbose_name = _("Group")
#         verbose_name_plural = _("Groups")

#     # def __str__(self):
#     #     """Return a human readable name when the object is printed."""
#     #     return self.id

#     def get_absolute_url(self):
#         """Return the absolute url."""
#         return reverse("group-detail-view", args=[str(self.pk)])


# class RunningNetwork(models.Model):
#     """
#     Model for Network.
#     """

#     rid = models.IntegerField()
#     instance = models.ForeignKey(
#         LabInstance,
#         on_delete=models.CASCADE,
#         related_name="node_networks",
#         editable=False,
#     )
#     running_description = models.CharField(
#         max_length=64,
#         editable=False,
#         verbose_name=_("Name"),
#         # validators=[AlphanumericValidator],
#         help_text=_("Network name."),
#     )
#     # running_type=link["type"]
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="node_networks", editable=False
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         """Database metadata."""

#         db_table = "networks"
#         # ordering = ["name"]
#         unique_together = [["user", "rid", "instance"]]
#         verbose_name = _("Network")
#         verbose_name_plural = _("Networks")

#     # def __str__(self):
#     #     """Return a human readable name when the object is printed."""
#     #     return self.name

#     def get_absolute_url(self):
#         """Return the absolute url."""
#         return reverse("network-detail-view", args=[str(self.pk)])


# class RunningNode(models.Model):
#     """
#     Model for Node.
#     """

#     rid = models.IntegerField()
#     instance = models.ForeignKey(
#         LabInstance,
#         on_delete=models.CASCADE,
#         related_name="nodes",
#         editable=False,
#     )
#     running_name = models.CharField(
#         max_length=64,
#         editable=False,
#         verbose_name=_("Name"),
#         validators=[AlphanumericValidator],
#         help_text=_("Node name."),
#     )
#     proxmox_host = models.ForeignKey(
#         ProxmoxHost,
#         on_delete=models.CASCADE,
#         related_name="nodes",
#         verbose_name=_("Proxmox host"),
#         help_text=_("Proxmox host associated with this node."),
#         blank=True,
#         null=True,
#     )
#     proxmox_id = models.IntegerField(
#         verbose_name=_("Proxmox node ID"),
#         help_text=_("Proxmox node ID associated with this node."),
#         blank=True,
#         null=True,
#     )
#     running_cpu = models.IntegerField(
#         default=1,
#         verbose_name=_("CPU"),
#         help_text=_("Minimum CPU required."),
#     )
#     running_ram = models.IntegerField(
#         default=2,
#         verbose_name=_("RAM"),
#         help_text=_("Minimum GB of RAM required."),
#     )
#     running_nics = models.IntegerField(
#         default=4,
#         verbose_name=_("NIC"),
#         help_text=_("Template default network interfaces."),
#     )
#     template = models.ForeignKey(
#         NodeTemplate,
#         on_delete=models.CASCADE,
#         related_name="nodes",
#         verbose_name=_("Template"),
#         help_text=_("Template associated with this node."),
#         editable=False,
#     )
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="nodes", editable=False
#     )
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         """Database metadata."""

#         db_table = "nodes"
#         ordering = ["running_name"]
#         unique_together = [
#             ["user", "rid", "instance"],
#         ]
#         verbose_name = _("Node")
#         verbose_name_plural = _("Nodes")

#     def __str__(self):
#         """Return a human readable name when the object is printed."""
#         return self.running_name

#     def get_absolute_url(self):
#         """Return the absolute url."""
#         return reverse("node-detail-view", args=[str(self.pk)])


# class RunningNodeInterface(models.Model):
#     """
#     Model for Interface.
#     """

#     rid = models.IntegerField()
#     node = models.ForeignKey(
#         Node,
#         on_delete=models.CASCADE,
#         related_name="node_interfaces",
#         editable=False,
#     )
#     running_description = models.CharField(
#         max_length=64,
#         verbose_name=_("Description"),
#         # validators=[AlphanumericValidator],
#         help_text=_("Interface description."),
#         blank=True,
#         null=True,
#     )
#     link = models.ForeignKey(
#         Network,
#         on_delete=models.SET_NULL,
#         related_name="node_interfaces",
#         blank=True,
#         null=True,
#     )

#     class Meta:
#         """Database metadata."""

#         db_table = "interfaces"
#         ordering = ["id"]
#         unique_together = [["node", "rid"]]
#         verbose_name = _("Interface")
#         verbose_name_plural = _("Interfaces")

#     # def __str__(self):
#     #     """Return a human readable name when the object is printed."""
#     #     return self.id

#     def get_absolute_url(self):
#         """Return the absolute url."""
#         return reverse("interface-detail-view", args=[str(self.pk)])
