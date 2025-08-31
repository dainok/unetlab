"""Define ORM models for Proxmox hosts."""

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from node.models import Node, NodeTemplate
from ui.include.validators import (
    AlphanumericPhraseValidator,
)

#############################################################################
# Lab HLD
#############################################################################

# class LabHLD:
#     def __init__(self, hld: dict | None = None):
#         self.hld = hld or {
#             "groups": [],
#             "interfaces": [],
#         }


#############################################################################
# Lab LLD
#############################################################################


class LabLld:
    groups: dict[str, dict] = {}
    nodes: dict[int, dict] = {}
    ifaces: dict[str, dict] = {}
    links: dict[int, dict] = {}
    node_name_to_id: dict[str, int] = {}

    def __init__(self, data: dict | None = None):
        if not data:
            pass
        elif "groups" in data and "interfaces" in data:
            # TODO: Validate HLD
            self.load_hld(data)
        elif "groups" in data and "nodes" in data and "links" in data:
            # TODO: validate LLD
            self.load_lld(data)
        else:
            raise ValidationError(
                "Data must contain either 'nodes'+'links' (LLD) or 'groups' (HLD)"
            )

        self._rebuild_maps()

    def _rebuild_maps(self):
        # Update node_name_to_id and interface_name_to_id
        self.node_name_to_id = {
            node["name"].lower(): node_id for node_id, node in self.nodes.items()
        }

    def _round_iface_count(self, count):
        return int(count / 4) + (count % 4 > 0) * 4

    def _get_template(self, template_prefix):
        qs = NodeTemplate.objects.filter(name__contains=template_prefix).order_by(
            "name"
        )
        # Prefer local template
        local_qs = qs.filter(repository__name="local")
        if local_qs:
            return local_qs.last()
        if qs:
            return qs.last()
        return None

    def _get_iface_index(self, node_id: int, iface_id: int):
        return f"{node_id}:{iface_id}"

    def load_hld(self, hld):
        for group_id, group_template in enumerate(hld.get("groups")):
            connect_hubs = group_template.get("connect_hubs", False)
            group_name = f"Group{group_id}"
            hub_count = group_template.get("hubs", 1)
            link_type = group_template.get("link_type", "l1")
            links = [link.split(",") for link in group_template.get("links", list())]
            node_count = group_template.get("count", 0)
            node_features = group_template.get("features", list())
            node_prefix = group_template.get("prefix", "")
            node_template = self._get_template(group_template.get("template", ""))
            topology = group_template.get("topology")

            print("-" * 78)
            print(group_name)
            print("-" * 78)
            print("LEN", len(self.nodes))

            if topology == "full-mesh":
                self._add_topology_full_mesh(
                    count=node_count,
                    features=node_features,
                    group=group_name,
                    link_type=link_type,
                    prefix=node_prefix,
                    template=node_template,
                )
            elif topology == "hub-spoke":
                continue
                self.add_topology_hub_spoke(
                    connect_hubs=connect_hubs,
                    count=node_count,
                    features=node_features,
                    group=group_name,
                    hub=hub_count,
                    link_type=link_type,
                    prefix=node_prefix,
                    template=node_template,
                )
            elif topology == "ring":
                continue
                self.add_topology_ring(
                    count=node_count,
                    features=node_features,
                    group=group_name,
                    link_type=link_type,
                    prefix=node_prefix,
                    template=node_template,
                )
            elif topology == "linear":
                continue
                self.add_topology_full_mesh(
                    count=node_count,
                    features=node_features,
                    group=group_name,
                    link_type=link_type,
                    prefix=node_prefix,
                    template=node_template,
                )
            elif topology == "custom":
                continue
                self.add_topology_full_mesh(
                    features=node_features,
                    group=group_name,
                    link_type=link_type,
                    links=links,
                    prefix=node_prefix,
                    template=node_template,
                )

    def add_group(self, group: str, members: list[int] = list()):
        group_index = group.lower()
        if group_index not in self.groups:
            self.groups[group_index] = {
                "name": group,
                "members": list(),
            }
        self.groups[group_index]["members"] = list(
            set(self.groups[group_index]["members"] + members)
        )

    def add_node(
        self,
        cpu: int,
        id: int,
        name: str,
        nics: int,
        ram: int,
        template: NodeTemplate,
        features: list = list(),
        group: str | None = None,
    ):
        self.nodes[id] = {
            "cpu": cpu,
            "features": features,
            "id": id,
            "name": name,
            "nics": nics,
            "ram": ram,
            "template": template.name,
        }
        self.add_group(group=group, members=[id])
        self._rebuild_maps()

    def add_node_from_template(
        self,
        features: list,
        group: str,
        prefix: str,
        template: NodeTemplate,
        nics: int = 0,
    ):

        # Find first available node_id
        node_id = 1
        used_node_ids = self.nodes.keys()
        while node_id in used_node_ids:
            node_id += 1

        nics = self._round_iface_count(nics)
        if nics < template.nics:
            nics = template.nics

        self.add_node(
            cpu=template.cpu,
            features=features,
            group=group,
            id=node_id,
            name=f"{prefix}{node_id}",
            nics=nics,
            ram=template.ram,
            template=template,
        )
        for iface_id in range(0, nics):
            self.add_interface(
                id=iface_id,
                name=f"Ethernet{iface_id}",
                node_id=node_id,
            )
        return node_id

    def add_interface(
        self,
        id: int,
        name: str,
        node_id: int,
        desc: str = "",
        features: list = list(),
        link_id: int | None = None,
    ):
        iface_index = self._get_iface_index(node_id=node_id, iface_id=id)
        self.ifaces[iface_index] = {
            "id": id,
            "name": name,
            "description": desc,
            "features": features,
            "link_id": link_id,
        }

    def connect(
        self,
        left_iface_id: int,
        left_node_id: int,
        right_iface_id: int,
        right_node_id: int,
        desc: str = "",
        kind: str = "l1",
    ):
        # Find first available link_id
        link_id = 0
        used_link_ids = self.links.keys()
        while link_id in used_link_ids:
            link_id += 1

        # Add link
        self.add_link(
            id=link_id,
            desc=desc,
            kind=kind,
        )

        # Attach interfaces to link
        left_iface_index = self._get_iface_index(
            node_id=left_node_id, iface_id=left_iface_id
        )
        self.ifaces[left_iface_index]["link_id"] = link_id
        right_iface_index = self._get_iface_index(
            node_id=right_node_id, iface_id=right_iface_id
        )
        self.ifaces[right_iface_index]["link_id"] = link_id
        return link_id

    def add_link(
        self,
        desc: str,
        id: int,
        kind: str,
    ):
        self.links[id] = {
            "description": desc,
            "id": id,
            "type": kind,
        }

    def _add_topology_full_mesh(
        self,
        count: int,
        features: list,
        group: str,
        link_type: str,
        prefix: str,
        template: NodeTemplate,
    ):
        required_links = count - 1
        if template.mgmt:
            required_links += 1

        # Nodes
        group_node_ids = []
        for i in range(count):
            group_node_ids.append(
                self.add_node_from_template(
                    features=features,
                    group=group,
                    nics=required_links,
                    prefix=prefix,
                    template=template,
                )
            )

        # Connect nodes in full-mesh
        starting_iface = 1 if template.mgmt else 0
        iface_counters = {node_id: starting_iface for node_id in group_node_ids}

        for index, left_node_id in enumerate(group_node_ids):
            for right_node_id in group_node_ids[index + 1 :]:
                left_iface_id = iface_counters[left_node_id]
                right_iface_id = iface_counters[right_node_id]
                left_node_name = self.nodes[left_node_id]["name"]
                right_node_name = self.nodes[right_node_id]["name"]
                left_iface_index = self._get_iface_index(
                    node_id=left_node_id, iface_id=left_iface_id
                )
                left_iface_name = self.ifaces[left_iface_index]
                right_iface_index = self._get_iface_index(
                    node_id=right_node_id, iface_id=right_iface_id
                )
                right_iface_name = self.ifaces[right_iface_index]["name"]
                link_desc = f"Link {left_node_name}:{left_iface_name} - {right_node_name}:{right_iface_name}"

                # Connect nodes
                self.connect(
                    left_iface_id=left_iface_id,
                    left_node_id=left_node_id,
                    desc=link_desc,
                    kind=link_type,
                    right_iface_id=right_iface_id,
                    right_node_id=right_node_id,
                )

                # Update inteface counters
                iface_counters[left_node_id] += 1
                iface_counters[right_node_id] += 1

    def get_lld(self):
        # Groups
        groups = []
        for group in self.groups.values():
            member_names = []
            for member_id in group["members"]:
                # Translate node_id to node_name
                member_names.append(self.nodes[member_id]["name"])
            group["members"] = member_names
            groups.append(group)

        # Nodes
        nodes = []
        for node in self.nodes.values():
            # Add interfaces
            node_id = node["id"]
            node["interfaces"] = []
            for iface_index, iface in self.ifaces.items():
                if iface_index.startswith(f"{node_id}:"):
                    node["interfaces"].append(iface)
            nodes.append(node)

        # Links
        links = list(self.links.values())

        return {
            "groups": groups,
            "nodes": nodes,
            "links": links,
        }

    #     for node_id, node in self.nodes.items():

    # def load_lld(data):
    #     for node in data.get("nodes"):
    #         self.add_node(node)
    #     for link in data.get("links"):
    #         self.add_link(link)
    #     for group in data("groups"):
    #         self.add_group(group)

    # ---- NODE MANAGEMENT ----
    # def add_node(self, node: dict):
    #     # TODO: validate node
    #     node_id = node["id"]
    #     node_interfaces = node.pop("interfaces")
    #     self._nodes[node_id] = node
    #     self._node_name_to_key[node["name"].lower()] = node_id

    #     node["interfaces"] = {
    #         node_interface["name"].lower(): node_interface for node_interface in node_interfaces
    #     }

    # def update_node(self, node_name: str, updates: dict):
    #     if node_id not in self.lld["nodes"]:
    #         raise ValidationError(f"Node {node_id} does not exist")
    #     self.lld["nodes"][node_id].update(updates)

    # def delete_node(self, node_id: int):
    #     if node_id not in self.lld["nodes"]:
    #         raise ValidationError(f"Node {node_id} does not exist")

    #     # rimuovi anche link associati
    #     links_to_remove = [lid for lid, l in self.lld["links"].items()
    #                        if any(nid == node_id for nid, _ in l["endpoints"])]
    #     for lid in links_to_remove:
    #         del self.lld["links"][lid]

    #     del self.lld["nodes"][node_id]

    # # ---- LINK MANAGEMENT ----
    # def add_link(self, link: dict):
    #     link_id = link.get("id")
    #     if not link_id:
    #         raise ValidationError("Link must have an 'id'")
    #     if link_id in self.lld["links"]:
    #         raise ValidationError(f"Link {link_id} already exists")

    #     endpoints = link.get("endpoints", [])
    #     if len(endpoints) != 2:
    #         raise ValidationError("Link must have exactly two endpoints")

    #     for nid, _ in endpoints:
    #         if nid not in self.lld["nodes"]:
    #             raise ValidationError(f"Node {nid} does not exist (link {link_id})")

    #     self.lld["links"][link_id] = link

    # def delete_link(self, link_id: int):
    #     if link_id not in self.lld["links"]:
    #         raise ValidationError(f"Link {link_id} does not exist")
    #     del self.lld["links"][link_id]

    # # ---- VALIDATION ----
    # def validate(self):
    #     # es: ogni link deve avere nodi validi
    #     for lid, link in self.lld["links"].items():
    #         if "endpoints" not in link:
    #             raise ValidationError(f"Link {lid} missing endpoints")
    #         for nid, _ in link["endpoints"]:
    #             if nid not in self.lld["nodes"]:
    #                 raise ValidationError(f"Link {lid} references missing node {nid}")

    #     return True

    # # ---- SERIALIZATION ----
    # def to_dict(self):
    #     return self.lld


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
