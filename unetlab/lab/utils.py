from lab.models import Lab
from node.models import NodeTemplate

"""
groups:
- template: local-vyos-vyos
  prefix: R
  count: 4
  topology: full-mesh
  link_type: l1
  features:
  - loopback:name=Loopback0
- template: local-vyos-vyos
  prefix: R
  count: 4
  topology: full-mesh
  link_type: l1
  features:
  - loopback:name=Loopback0
- template: local-vyos-vyos
  prefix: R
  count: 6
  topology: hub-spoke
  hubs: 2
  link_type: l1
  features:
  - loopback:name=Loopback0
interfaces:
- match: Loopback0
  address: 192.168.0.1/16
  mask: 32
  features:
  - ospf:area=0
- match: Ethernet
  address: 10.0.0.0/8
  mask: auto
  features:
  - ospf:area=0
"""


def get_management_interface(teplate):
    pass


def get_interface_name(template, id):
    return f"Ethernet{id}"
    pass


def get_template(prefix):
    qs = NodeTemplate.objects.filter(name__contains=prefix).order_by("name")
    # Prefer local template
    local_qs = qs.filter(repository__name="local")
    if local_qs:
        return local_qs.last()
    if qs:
        return qs.last()
    return None


def round_interface_count(interface_count):
    return int(interface_count / 4) + (interface_count % 4 > 0) * 4


def make_topology_full_mesh(
    node_id: int = 1,
    link_id: int = 1,
    prefix: str = "R",
    count: int = 4,
    template: str = "",
    features: list = list(),
    link_type: str = "l1",
):
    """
    Genera una topologia full-mesh.

    :param hld: dict con chiavi:
        - topology: full-mesh
        - prefix (es: "R")
        - count (numero totale di nodi)
        - template
        - type (es: "l1")
        - features (lista di stringhe)
    :return: (nodes, links)
    """

    template_obj = get_template(template)
    if not template_obj:
        raise ValueError("Template not found")

    # nodi
    nodes = []
    for i in range(count):
        nodes.append(
            {
                "id": node_id,
                "name": f"{prefix}{node_id}",
                "cpu": template_obj.cpu,
                "ram": template_obj.ram,
                "nics": round_interface_count(
                    count
                ),  # number of nodes - 1 + management
                "template": template_obj.name,
                "features": features,
                "interfaces": [],
            }
        )
        node_id += 1

    # connect nodes in full-mesh
    links = []
    for i in range(count):
        for j in range(i + 1, count):
            n1 = nodes[i]
            n2 = nodes[j]

            n1_if = {
                "id": len(n1["interfaces"]),
                "link_id": link_id,
                "name": f"Ethernet{len(n1['interfaces'])}",
            }
            n2_if = {
                "id": len(n2["interfaces"]),
                "link_id": link_id,
                "name": f"Ethernet{len(n2['interfaces'])}",
            }

            n1["interfaces"].append(n1_if)
            n2["interfaces"].append(n2_if)

            links.append(
                {
                    "id": link_id,
                    "name": f"{n1['name']}:{n1_if['name']} - {n2['name']}:{n2_if['name']}",
                    "type": link_type,
                }
            )
            link_id += 1

    return nodes, links


def make_topology_linear():
    pass


def make_topology_ring():
    pass


def make_topology_hub_spoke(
    node_id: int = 1,
    link_id: int = 1,
    prefix: str = "R",
    count: int = 3,
    hubs: int = 1,
    connect_hubs: bool = False,
    template: str = "",
    features: list = list(),
    link_type: str = "l1",
):
    """
    Genera una topologia hub-spoke.

    :param hld: dict con chiavi:
        - topology: hub-spoke
        - prefix (es: "R")
        - count (numero totale di nodi)
        - hubs (numero di hub)
        - connect_hubs: True
        - template
        - type (es: "l1")
        - features (lista di stringhe)
    :return: (nodes, links)
    """
    template_obj = get_template(template)
    if not template_obj:
        raise ValueError("Template not found")

    # nodi
    nodes = []
    for i in range(count):
        nodes.append(
            {
                "id": node_id,
                "name": f"{prefix}{node_id}",
                "cpu": template_obj.cpu,
                "ram": template_obj.ram,
                "nics": round_interface_count(count),
                "template": template_obj.name,
                "features": features,
                "interfaces": [],
            }
        )
        node_id += 1

    # spokes (dopo gli hub) collegati a tutti gli hub
    links = []
    for spoke_idx in range(hubs, count):
        spoke = nodes[spoke_idx]
        for hub_idx in range(hubs):
            hub = nodes[hub_idx]

            hub_if = {
                "id": len(hub["interfaces"]),
                "link_id": link_id,
                "name": f"Ethernet{len(hub['interfaces'])}",
            }
            spoke_if = {
                "id": len(spoke["interfaces"]),
                "link_id": link_id,
                "name": f"Ethernet{len(spoke['interfaces'])}",
            }

            hub["interfaces"].append(hub_if)
            spoke["interfaces"].append(spoke_if)

            links.append(
                {
                    "id": link_id,
                    "name": f"{hub['name']}:{hub_if['name']} - {spoke['name']}:{spoke_if['name']}",
                    "type": link_type,
                }
            )
            link_id += 1

    # opzionale: link tra hub
    if connect_hubs and hubs > 1:
        for i in range(hubs):
            for j in range(i + 1, hubs):
                hub1 = nodes[i]
                hub2 = nodes[j]

                hub1_if = {
                    "id": len(hub1["interfaces"]),
                    "link_id": link_id,
                    "name": f"Ethernet{len(hub1['interfaces'])}",
                }
                hub2_if = {
                    "id": len(hub2["interfaces"]),
                    "link_id": link_id,
                    "name": f"Ethernet{len(hub2['interfaces'])}",
                }

                hub1["interfaces"].append(hub1_if)
                hub2["interfaces"].append(hub2_if)

                links.append(
                    {
                        "id": link_id,
                        "name": f"{hub1['name']}:{hub1_if['name']} - {hub2['name']}:{hub2_if['name']}",
                        "type": link_type,
                    }
                )
                link_id += 1

    return nodes, links


def build_lld(lab_id):
    lab = Lab.objects.get(pk=lab_id)
    hld = lab.hld
    lld = {
        "groups": [],
        "nodes": [],
        "links": [],
    }
    nodes = dict()
    links = dict()
    groups = hld.get("groups", list())

    link_id = 1
    node_id = 1

    # Add gruop
    for group_id, group_template in enumerate(groups):
        topology_params = group_template.copy()
        topology_params["node_id"] = node_id
        topology_params["link_id"] = link_id
        topology = topology_params.pop("topology")
        if topology == "full-mesh":
            nodes, links = make_topology_full_mesh(**topology_params)
        elif topology == "hub-spoke":
            nodes, links = make_topology_hub_spoke(**topology_params)
        else:
            raise ValueError("Topology not supported")

        # Builing group:
        lld["nodes"] += nodes
        lld["links"] += links
        lld["groups"].append(
            {
                "id": group_id,
                "name": f"Group{group_id}",
                "members": [node["name"] for node in nodes],
            }
        )
        node_id += len(nodes)
        link_id += len(links)

    lab.lld = lld
    lab.save()
