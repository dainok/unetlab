
from lab.models import Lab
from node.models import NodeTemplate

"""
groups:
- template: local-vyos-vyos
  prefix: R
  count: 4
  topology: full-mesh
  type: l2
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
    qs = NodeTemplate.objects.filter(name__contains=prefix)
    if qs:
        return qs.first()
    return None



def build_lld(lab_id):
    lab = Lab.objects.get(pk=lab_id)
    hld = lab.hld
    node_names = []
    nodes = {}
    interfaces = {}
    links = {}
    groups = {}

    link_id = 1
    node_id = 1
    group_id = 1
    for group_template in hld.get("groups", []):
        # For each group
        group_nodes = []
        template_prefix = group_template.get("template")
        if not template_prefix:
            raise ValueError("Template è obbligatorio")
        count = group_template.get("count", 1)
        prefix = group_template.get("prefix", "N")
        features = group_template.get("features")
        topology = group_template.get("topology")
        link_type = group_template.get("type", "l2")
        template_obj = get_template(template_prefix)
        if not template_obj:
            raise ValueError("Template non trovato")
        
        # Create nodes
        for counter in range(1, count + 1):
            # Create unique name
            name_counter = counter
            while True:
                name = f"{ prefix }{ name_counter }"
                if name not in node_names:
                    node_names.append(name)
                    break
                name_counter += 1
            
            # Create node
            node = {
                "id": node_id,
                "template": template_obj.name,
                "name": name,
            }
            if features:
                node["features"] = features


            nodes[node_id] = node
            group_nodes.append(node)
            node_id += 1

            # Builing group
            for node in group_nodes:
                group_name = f"Group{group_id}"
                if not group_name in groups:
                    groups[group_name] = []
                groups[f"Group{group_id}"].append(node["name"])



        group_id += 1

        if topology == "full-mesh":
            for i in range(len(group_nodes)):
                node_left = group_nodes[i]
                # print(node_left)
                for j in range(i+1, len(group_nodes)):
                    node_right = group_nodes[j]
                    # print(node_right)

                    # Prendiamo la prima interfaccia disponibile per ciascun nodo
                    node_id_left = node_left["id"]
                    node_name_left = node_left["name"]
                    iface_id_left = len(interfaces.get(node_id_left, {}))
                    iface_name_left = get_interface_name(node_left["template"], iface_id_left)
                    node_id_right = node_right["id"]
                    node_name_right = node_right["name"]
                    iface_id_right = len(interfaces.get(node_id_right, {}))
                    iface_name_right = get_interface_name(node_right["template"], iface_id_right)

                    # Define network
                    links[link_id] = {
                        "id": link_id,
                        "name": f"{node_name_left}:{iface_name_left} - {node_name_right}:{iface_name_right}",
                        "type": link_type,
                    }

                    # Adding interface to link
                    if not node_id_left in interfaces:
                        interfaces[node_id_left] = []
                    interfaces[node_id_left].append({
                        "id": iface_id_left,
                        "name": iface_name_left,
                        "link_id": link_id
                    })
                    if not node_id_right in interfaces:
                        interfaces[node_id_right] = []
                    interfaces[node_id_right].append({
                        "id": iface_id_right,
                        "name": iface_name_right,
                        "link_id": link_id
                    })

                    link_id += 1



    # Builing LLD
    lld = {
        "groups": [],
        "nodes": [],
        "links": [],
    }

    for node_id, node in nodes.items():
        node["interfaces"] = interfaces[node_id]
        lld["nodes"].append(node)
    for link_id, link in links.items():
        lld["links"].append(link)
    for group_name, group_members in groups.items():
        lld["groups"].append({
            "name": group_name,
            "members": group_members
        })

    lab.lld = lld
    lab.save()
    # from pprint import pprint
    # pprint(lld)


