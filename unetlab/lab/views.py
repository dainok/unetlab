"""Views for Lab app."""

import yaml
from django.db import transaction
from django.db.models import query, Q
from rest_framework.decorators import action
from rest_framework.response import Response
from lab.models import Lab

# from lab.utils import LabLld
from lab.filters import LabFilter
from lab.forms import LabForm
from lab.permissions import LabPermissionPolicy
from lab.serializers import (
    LabSerializer,
    # LabInstanceDetailSerializer,
    # LabInstanceListSerializer,
)
from lab.tables import LabTable
from ui.include.views import (
    APICRUDViewSet,
    ObjectBulkDeleteView,
    ObjectChangeView,
    ObjectCreateView,
    ObjectDeleteView,
    ObjectDetailView,
    ObjectListView,
)


#############################################################################
# Lab
#############################################################################


class LabQueryMixin:
    """Mixin encapsulating common queryset and permission logic for Lab objects."""

    filterset_class = LabFilter
    form_class = LabForm
    model = Lab
    policy_class = LabPermissionPolicy
    serializer_class = LabSerializer
    table_class = LabTable

    def get_queryset(self) -> query.QuerySet:
        """Return the queryset of Lab objects accessible to the current user."""
        qs = Lab.objects.all()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all Lab objects
            return qs
        # Staff and standard users can see users who share at least one group
        groups = user.groups.all()
        return qs.filter(Q(shared_group__in=groups) | Q(user=user)).distinct()


class LabAPIViewSet(LabQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the Lab model."""

    def perform_create(self, serializer):
        """Set user when creating a new lab."""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='build')
    def build(self, request, pk=None):
        """Build LLD from HLD."""
        lab = self.get_object()

        with transaction.atomic():
            lab.rebuild()

        serializer = self.get_serializer(lab)
        return Response(serializer.data)


class LabBulkDeleteView(LabQueryMixin, ObjectBulkDeleteView):
    """HTML view for deleting multiple Lab objects at once."""


class LabChangeView(LabQueryMixin, ObjectChangeView):
    """HTML view for updating an existing Lab."""


class LabCreateView(LabQueryMixin, ObjectCreateView):
    """HTML view for creating a new Lab."""


class LabDeleteView(LabQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single GLabroup."""


class LabDetailView(LabQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a Lab."""

    exclude = ['id']
    sequence = ['name', 'user', 'shared_group', 'created_at', 'updated_at']
    template_name = 'lab_detail.html'

    def get_context_data(self, **kwargs):
        """Prepare HLD/LLD data for rendering."""
        context = super().get_context_data(**kwargs)
        lab = self.object

        if lab.hld:
            # Convert JSON into YAML
            context['hld_yaml'] = yaml.safe_dump(
                lab.hld,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
                indent=2,
            )
        else:
            context['hld_yaml'] = ''
        return context


class LabListView(LabQueryMixin, ObjectListView):
    """HTML view for displaying a table of Lab objects."""


# class LabTopologyView(LabQueryMixin, ObjectDetailView):
#     model = Lab
#     template_name = "lab_topology.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         lab = self.object

#         # Creo un array per i link nella forma src-dst
#         if lab.lld:
#             cy_nodes = [
#                 {
#                     "data": {
#                         "id": node["name"],
#                         "label": node["name"],
#                         "image_url": "/static/icons/router.svg",
#                     },
#                 }
#                 for node in lab.lld.get("nodes", [])
#             ]
#             cy_edges = []

#             link_map = {}
#             for node in lab.lld.get("nodes", []):
#                 for iface in node["interfaces"]:
#                     link_map.setdefault(iface["link_id"], []).append(
#                         {"node": node["name"], "iface_name": iface["name"]}
#                     )
#             for link in lab.lld.get("links", []):
#                 endpoints = link_map.get(link["id"], [])
#                 if len(endpoints) == 2:
#                     cy_edges.append(
#                         {
#                             "data": {
#                                 # "id": f"link{link['id']}",
#                                 "source": endpoints[0]["node"],
#                                 "target": endpoints[1]["node"],
#                                 "source_label": endpoints[0]["iface_name"],
#                                 "target_label": endpoints[1]["iface_name"],
#                             }
#                         }
#                     )
#                 elif len(endpoints) > 2:
#                     # Add network as node
#                     cy_nodes.append(
#                         {
#                             "data": {
#                                 "id": f"Link{link['id']}",
#                                 "label": f"N{link['id']}",
#                                 "image_url": "/static/icons/l2-switch.svg",
#                             },
#                         }
#                     )
#                     for endpoint in endpoints:
#                         cy_edges.append(
#                             {
#                                 "data": {
#                                     # "id": f"link{link['id']}",
#                                     "source": endpoint["node"],
#                                     "target": f"Link{link['id']}",
#                                     "source_label": endpoint["iface_name"],
#                                 }
#                             }
#                         )
#             context["elements"] = cy_nodes + cy_edges
#         return context


#############################################################################
# Instance
#############################################################################


# class LabInstanceQueryMixin:
#     """Mixin to encapsulate common Template queryset and permissions logic.

#     Used by both UI and API views.
#     """

#     serializer_detail_class = LabInstanceDetailSerializer
#     serializer_list_class = LabInstanceListSerializer

#     # def get_serializer_class(self):
#     #     """Usa un serializer diverso per list e detail."""
#     #     if self.action == "list":
#     #         return LabInstanceListSerializer
#     #     return LabInstanceDetailSerializer

#     def get_queryset(self):
#         """Return the queryset of `User` objects accessible to the current user.

#         - Superusers can access all `User` objects.
#         - Staff users can see users who share at least one group
#         - Non-superusers can only access their own `User` object.
#         """
#         qs = LabInstance.objects.all()
#         user = self.request.user
#         if user.is_superuser:
#             # Admin users can see all `User` objects
#             return qs
#         if user.is_staff:
#             # Staff users can see users who share at least one group
#             groups = user.groups.all()
#             return qs.filter(user__groups__in=groups).distinct()
#         # Non-admin users can only see their own user
#         return qs.filter(user=user)

#     def get_object(self):
#         """Return a `User` object only if the user has permission.

#         - Superusers can access any `User`.
#         - Staff users can see users who share at least one group.
#         - Non-superusers can only access their own `User` object.

#         Raises:
#             PermissionDenied: If the user does not have access.
#         """
#         # obj = self.get_queryset().filter(pk=self.kwargs["pk"]).prefetch_related("node_groups", "nodes", "node_networks").get()
#         obj = super().get_object()
#         print("AAA")
#         print(obj)
#         print(obj.nodes.all())
#         user = self.request.user
#         if user.is_superuser:
#             # Admin users can see all `User` objects
#             return obj
#         if user.is_staff:
#             if user.groups.filter(
#                 pk__in=obj.groups.values_list("pk", flat=True)
#             ).exists():
#                 return obj
#         if user == obj:
#             # Non-admin users can only see the `Group` objects they belong to
#             return obj
#         raise PermissionDenied(messages.PERMISSION_DENIED)


# class LabInstanceAPIViewSet(LabInstanceQueryMixin, APICRUDViewSet):
#     """REST API endpoints for Template model."""

#     # serializer_class = LabInstanceSerializer
#     filterset_class = LabInstanceFilter

#     # def get_serializer_class(self):
#     #     """Usa un serializer diverso per list e detail."""
#     #     if self.action == "list":
#     #         return LabInstanceListSerializer
#     #     return LabInstanceDetailSerializer

#     def perform_create(self, serializer):
#         # Set user and lab ID
#         lab_id = self.request.data.get("lab_id")
#         lab_obj = Lab.objects.get(id=lab_id)
#         lab_instance_obj = serializer.save(user=self.request.user, lab=lab_obj)

#         if not lab_obj.lld:
#             # Create LLD from HLD
#             lld = LabLld()
#             lld.load_hld(lab_obj.hld)
#             lab_obj.lld = lld.to_dict()
#             lab_obj.save()
#         print("HERE")
#         print(lab_obj.lld)
#         for link in lab_obj.lld["links"]:
#             Network.objects.create(
#                 rid=link["id"],
#                 instance=lab_instance_obj,
#                 user=self.request.user,
#                 running_description=link["description"],
#                 # running_type=link["type"],
#             )

#         for node in lab_obj.lld["nodes"]:
#             template = NodeTemplate.objects.get(name=node["template"])
#             Node.objects.create(
#                 rid=node["id"],
#                 instance=lab_instance_obj,
#                 running_cpu=node["cpu"],
#                 running_name=node["name"],
#                 running_ram=node["ram"],
#                 running_nics=node["nics"],
#                 template=template,
#                 user=self.request.user,
#             )
#             # for iface in node["interfaces"]:
#             #     network_obj = Network.objects.get(user=self.request.user, instance=lab_instance_obj, rid=iface["link_id"])
#             #     NodeInterface.objects.create(
#             #         rid=iface["id"],
#             #         running_name=iface["name"],
#             #         running_description=iface["description"],
#             #         link=network_obj,
#             #     )

#         # NodeGroup
#         # print(lab_obj.lld["groups"])
#         # [{'name': 'Group0', 'members': ['R1', 'R2', 'R3', 'R4']}, {'name': 'Group1', 'members': ['R8', 'R5', 'R6', 'R7']}, {'name': 'Group2', 'members': ['R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17', 'R18', 'R19']}, {'name': 'Group3', 'members': ['R20', 'R21', 'R22', 'R23', 'R24', 'R25']}, {'name': 'Group4', 'members': ['R26', 'R27', 'R28', 'R29']}, {'name': 'Group5', 'members': ['R32', 'R33', 'R10', 'R11', 'R30', 'R31']}, {'name': 'Group6', 'members': ['R1', 'R2', 'R5', 'R6', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17', 'R18', 'R19', 'R20', 'R23', 'R26', 'R29']}]
#         # print(lab_obj.lld["links"])
#         # [{'description': 'Link R1:Ethernet1 R2:Ethernet1', 'id': 0, 'type': 'l1'}, {'description': 'Link R1:Ethernet2 R3:Ethernet1', 'id': 1, 'type': 'l1'}, {'description': 'Link R1:Ethernet3 R4:Ethernet1', 'id': 2, 'type': 'l1'}, {'description': 'Link R2:Ethernet2 R3:Ethernet2', 'id': 3, 'type': 'l1'}, {'description': 'Link R2:Ethernet3 R4:Ethernet2', 'id': 4, 'type': 'l1'}, {'description': 'Link R3:Ethernet3 R4:Ethernet3', 'id': 5, 'type': 'l1'}, {'description': 'Link R5:Ethernet1 R6:Ethernet1', 'id': 6, 'type': 'l1'}, {'description': 'Link R5:Ethernet2 R7:Ethernet1', 'id': 7, 'type': 'l1'}, {'description': 'Link R5:Ethernet3 R8:Ethernet1', 'id': 8, 'type': 'l1'}, {'description': 'Link R6:Ethernet2 R7:Ethernet2', 'id': 9, 'type': 'l1'}, {'description': 'Link R6:Ethernet3 R8:Ethernet2', 'id': 10, 'type': 'l1'}, {'description': 'Link R7:Ethernet3 R8:Ethernet3', 'id': 11, 'type': 'l1'}, {'description': 'Link R9:Ethernet1 R12:Ethernet1', 'id': 12, 'type': 'l1'}, {'description': 'Link R10:Ethernet1 R12:Ethernet2', 'id': 13, 'type': 'l1'}, {'description': 'Link R11:Ethernet1 R12:Ethernet3', 'id': 14, 'type': 'l1'}, {'description': 'Link R9:Ethernet2 R13:Ethernet1', 'id': 15, 'type': 'l1'}, {'description': 'Link R10:Ethernet2 R13:Ethernet2', 'id': 16, 'type': 'l1'}, {'description': 'Link R11:Eth
#         # {'cpu': 1, 'features': [], 'id': 32, 'name': 'R32', 'nics': 4, 'ram': 2, 'template': 'template-local-vyos-vyos-2025.07.28-0022-unl',
#         # 'interfaces': [{'id': 0, 'name': 'Ethernet0', 'description': 'OOB Management', 'features': [], 'link_id': None}, {'id': 1, 'name': 'Ethernet1', 'description': '', 'features': [], 'link_id': 48}, {'id': 2, 'name': 'Ethernet2', 'description': '', 'features': [], 'link_id': 50}, {'id': 3, 'name': 'Ethernet3', 'description': '', 'features': [], 'link_id': 51}]}

#         print("BUILDING NODES AND  NETWORKS")


# class LabInstanceBulkDeleteView(LabInstanceQueryMixin, ObjectBulkDeleteView):
#     """HTML view for deleting multiple `User` objects at once."""

#     model = LabInstance


# # class LabInstanceChangeView(LabInstanceQueryMixin, ObjectChangeView):
# #     """HTML view for updating an existing `User`."""

# #     model = LabInstance
# #     form_class = LabInstanceForm


# class LabInstanceCreateView(LabQueryMixin, ObjectCreateView):
#     """HTML view for creating a new `User`."""

#     model = LabInstance
#     form_class = LabInstanceForm


# class LabInstanceDeleteView(LabInstanceQueryMixin, ObjectDeleteView):
#     """HTML view for deleting a single `User`."""

#     model = LabInstance


# class LabInstanceDetailView(LabInstanceQueryMixin, ObjectDetailView):
#     model = LabInstance
#     template_name = "instance_detail.html"

#     # def get_context_data(self, **kwargs):
#     #     ctx = super().get_context_data(**kwargs)
#     #     # aggiunge una versione semplice per debug
#     #     ctx["nodes_debug"] = list(self.object.nodes.values("id", "running_name"))
#     #     print(ctx)
#     #     print(type(ctx["object"]))
#     #     return ctx


# class LabInstanceListView(LabInstanceQueryMixin, ObjectListView):
#     model = LabInstance
#     table_class = LabInstanceTable
#     filterset_class = LabInstanceFilter
