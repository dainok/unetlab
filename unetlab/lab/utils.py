"""Utility functions for the lab app."""

from django.core.exceptions import ValidationError
from node.models import NodeTemplate


#############################################################################
# Lab LLD
#############################################################################


class LabLld:
    groups: dict[str, dict] = {}
    nodes: dict[int, dict] = {}
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
        return (int(count / 4) + (count % 4 > 0)) * 4

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
                self._add_topology_hub_spoke(
                    connect_hubs=connect_hubs,
                    count=node_count,
                    features=node_features,
                    group=group_name,
                    hubs=hub_count,
                    link_type=link_type,
                    prefix=node_prefix,
                    template=node_template,
                )
            elif topology == "ring":
                self._add_topology_ring(
                    count=node_count,
                    features=node_features,
                    group=group_name,
                    link_type=link_type,
                    prefix=node_prefix,
                    template=node_template,
                )
            elif topology == "linear":
                self._add_topology_linear(
                    count=node_count,
                    features=node_features,
                    group=group_name,
                    link_type=link_type,
                    prefix=node_prefix,
                    template=node_template,
                )
            elif topology == "custom":
                self._add_topology_custom(
                    features=node_features,
                    group=group_name,
                    link_type=link_type,
                    links=links,
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
        ram: int,
        template: NodeTemplate,
        features: list = list(),
        group: str | None = None,
        nics: int = 0,
    ):
        self.nodes[id] = {
            "cpu": cpu,
            "features": features,
            "id": id,
            "interfaces": {},
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
        template: NodeTemplate,
        name: str | None = None,
        oob: bool = True,
        prefix: str | None = None,
    ):
        # Find first available node_id
        node_id = 1
        used_node_ids = self.nodes.keys()
        while node_id in used_node_ids:
            node_id += 1

        if prefix:
            name = f"{prefix}{node_id}"
        self.add_node(
            cpu=template.cpu,
            features=features,
            group=group,
            id=node_id,
            name=name,
            ram=template.ram,
            template=template,
        )
        if oob:
            self.add_interface(id=0, node_id=node_id, desc="OOB Management")
        return node_id

    def add_interface(
        self,
        id: int,
        node_id: int,
        desc: str = "",
        features: list = list(),
        link_id: int | None = None,
    ):
        name = f"Ethernet{id}"
        self.nodes[node_id]["interfaces"][id] = {
            "id": id,
            "name": name,
            "description": desc,
            "features": features,
            "link_id": link_id,
        }

        # Update node interfaces
        self.nodes[node_id]["nics"] = len(self.nodes[node_id]["interfaces"])

    def connect(
        self,
        node_ids: list[int],
        kind: str = "l1",
    ):
        # Find first available link_id
        link_id = 0
        used_link_ids = self.links.keys()
        while link_id in used_link_ids:
            link_id += 1

        # Add link
        desc = "Link"
        for node_id in node_ids:
            # Add interface to link
            node_name = self.nodes[node_id]["name"]
            iface_id = len(self.nodes[node_id]["interfaces"])
            iface_name = f"Ethernet{iface_id}"
            self.add_interface(id=iface_id, node_id=node_id, link_id=link_id)
            desc += f" {node_name}:{iface_name}"
        self.add_link(
            id=link_id,
            desc=desc,
            kind=kind,
        )

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
        if not template:
            raise ValueError("Template is mandatory")
        
        # Nodes
        group_node_ids = []
        for i in range(count):
            group_node_ids.append(
                self.add_node_from_template(
                    features=features,
                    group=group,
                    oob=template.oob,
                    prefix=prefix,
                    template=template,
                )
            )

        # Connect nodes in full-mesh
        for index, left_node_id in enumerate(group_node_ids):
            for right_node_id in group_node_ids[index + 1 :]:
                # Connect nodes
                self.connect(
                    node_ids=[left_node_id, right_node_id],
                    kind=link_type,
                )

    def _add_topology_hub_spoke(
        self,
        count: int,
        features: list,
        group: str,
        link_type: str,
        prefix: str,
        template: NodeTemplate,
        connect_hubs: bool = False,
        hubs: int = 1,
    ):
        if not template:
            raise ValueError("Template is mandatory")
        
        # Hubs
        group_hub_ids = []
        for i in range(hubs):
            group_hub_ids.append(
                self.add_node_from_template(
                    features=features,
                    group=group,
                    oob=template.oob,
                    prefix=prefix,
                    template=template,
                )
            )

        # Spokes
        group_spoke_ids = []
        for i in range(count):
            group_spoke_ids.append(
                self.add_node_from_template(
                    features=features,
                    group=group,
                    oob=template.oob,
                    prefix=prefix,
                    template=template,
                )
            )

        for spoke_id in group_spoke_ids:
            for hub_id in group_hub_ids:
                # Connect nodes
                self.connect(
                    node_ids=[hub_id, spoke_id],
                    kind=link_type,
                )

        # Connect hubs
        if hubs > 1 and connect_hubs:
            for index, left_hub_id in enumerate(group_hub_ids):
                for right_hub_id in group_hub_ids[index + 1 :]:
                    # Connect hubs
                    self.connect(
                        node_ids=[left_hub_id, right_hub_id],
                        kind=link_type,
                    )

    def _add_topology_ring(
        self,
        count: int,
        features: list,
        group: str,
        link_type: str,
        prefix: str,
        template: NodeTemplate,
    ):
        if not template:
            raise ValueError("Template is mandatory")
        
        # Nodes
        group_node_ids = []
        for i in range(count):
            group_node_ids.append(
                self.add_node_from_template(
                    features=features,
                    group=group,
                    oob=template.oob,
                    prefix=prefix,
                    template=template,
                )
            )

        # Connect nodes in ring
        for i in range(count):
            left_node_id = group_node_ids[i]
            right_node_id = group_node_ids[(i + 1) % count]

            # Connect nodes
            self.connect(
                node_ids=[left_node_id, right_node_id],
                kind=link_type,
            )

    def _add_topology_linear(
        self,
        count: int,
        features: list,
        group: str,
        link_type: str,
        prefix: str,
        template: NodeTemplate,
    ):
        if not template:
            raise ValueError("Template is mandatory")
        
        # Nodes
        group_node_ids = []
        for i in range(count):
            group_node_ids.append(
                self.add_node_from_template(
                    features=features,
                    group=group,
                    oob=template.oob,
                    prefix=prefix,
                    template=template,
                )
            )

        for i in range(count - 1):
            left_node_id = group_node_ids[i]
            right_node_id = group_node_ids[i + 1]

            # Connect nodes
            self.connect(
                node_ids=[left_node_id, right_node_id],
                kind=link_type,
            )

    def _add_topology_custom(
        self,
        features: list,
        group: str,
        link_type: str,
        links: list[str],
        template: NodeTemplate,
    ):
        for link in links:
            link_node_ids = []
            for node_name in link:
                node_key = node_name.lower().strip()
                node_name = node_name.strip()
                if node_key in self.node_name_to_id:
                    node_id = self.node_name_to_id[node_key]
                else:
                    if not template:
                        raise ValueError("Template is mandatory")
                    node_id = self.add_node_from_template(
                        features=features,
                        group=group,
                        oob=template.oob,
                        name=node_name,
                        template=template,
                    )
                link_node_ids.append(node_id)

            self.connect(node_ids=link_node_ids, kind=link_type)
            self.add_group(group=group, members=link_node_ids)

    def to_dict(self):
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
            node_ifaces = node.pop("interfaces")
            node["interfaces"] = []
            for iface_id, iface in node_ifaces.items():
                node["interfaces"].append(iface)
            nodes.append(node)

        # Links
        links = list(self.links.values())

        return {
            "groups": groups,
            "nodes": nodes,
            "links": links,
        }
