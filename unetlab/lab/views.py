"""Views, called by URLs."""

import yaml
from django.core.exceptions import PermissionDenied
from lab.models import Lab, LabInstance
from lab.serializers import LabSerializer, LabInstanceSerializer
from lab.filters import LabFilter, LabInstanceFilter
from lab.forms import LabForm, LabInstanceForm
from lab.tables import LabTable, LabInstanceTable
from ui.include import messages
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
    """Mixin to encapsulate common Template queryset and permissions logic.

    Used by both UI and API views.
    """

    def get_queryset(self):
        """Return the queryset of `User` objects accessible to the current user.

        - Superusers can access all `User` objects.
        - Staff users can see users who share at least one group
        - Non-superusers can only access their own `User` object.
        """
        qs = Lab.objects.all()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `User` objects
            return qs
        if user.is_staff:
            # Staff users can see users who share at least one group
            groups = user.groups.all()
            return qs.filter(user__groups__in=groups).distinct()
        # Non-admin users can only see their own user
        return qs.filter(user=user)

    def get_object(self):
        """Return a `User` object only if the user has permission.

        - Superusers can access any `User`.
        - Staff users can see users who share at least one group.
        - Non-superusers can only access their own `User` object.

        Raises:
            PermissionDenied: If the user does not have access.
        """
        obj = super().get_object()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `User` objects
            return obj
        if user.is_staff:
            if user.groups.filter(
                pk__in=obj.groups.values_list("pk", flat=True)
            ).exists():
                return obj
        if user == obj:
            # Non-admin users can only see the `Group` objects they belong to
            return obj
        raise PermissionDenied(messages.PERMISSION_DENIED)


class LabAPIViewSet(LabQueryMixin, APICRUDViewSet):
    """REST API endpoints for Template model."""

    serializer_class = LabSerializer
    filterset_class = LabFilter

    def perform_create(self, serializer):
        # Set user
        serializer.save(user=self.request.user)


class LabBulkDeleteView(LabQueryMixin, ObjectBulkDeleteView):
    """HTML view for deleting multiple `User` objects at once."""

    model = Lab


class LabChangeView(LabQueryMixin, ObjectChangeView):
    """HTML view for updating an existing `User`."""

    model = Lab
    form_class = LabForm


class LabCreateView(LabQueryMixin, ObjectCreateView):
    """HTML view for creating a new `User`."""

    model = Lab
    form_class = LabForm


class LabDeleteView(LabQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single `User`."""

    model = Lab


class LabDetailView(LabQueryMixin, ObjectDetailView):
    model = Lab
    exclude = ["id"]
    sequence = ["name", "created_at", "description"]
    template_name = "lab_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab = self.object

        # Trasformo JSONField hld → YAML string
        if lab.hld:
            # JSON → YAML
            context["hld_yaml"] = yaml.safe_dump(
                lab.hld,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
                indent=2,
            )
        else:
            context["hld_yaml"] = ""
        return context


class LabListView(LabQueryMixin, ObjectListView):
    model = Lab
    table_class = LabTable
    filterset_class = LabFilter


class LabTopologyView(LabQueryMixin, ObjectDetailView):
    model = LabInstance
    template_name = "lab_topology.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lab = self.object

        # Creo un array per i link nella forma src-dst
        if lab.lld:
            cy_nodes = [
                {
                    "data": {
                        "id": node["name"],
                        "label": node["name"],
                        "image_url": "/static/icons/router.svg",
                    },
                }
                for node in lab.lld.get("nodes", [])
            ]
            cy_edges = []

            link_map = {}
            for node in lab.lld.get("nodes", []):
                for iface in node["interfaces"]:
                    link_map.setdefault(iface["link_id"], []).append(
                        {"node": node["name"], "iface_name": iface["name"]}
                    )
            for link in lab.lld.get("links", []):
                endpoints = link_map.get(link["id"], [])
                if len(endpoints) == 2:
                    cy_edges.append(
                        {
                            "data": {
                                # "id": f"link{link['id']}",
                                "source": endpoints[0]["node"],
                                "target": endpoints[1]["node"],
                                "source_label": endpoints[0]["iface_name"],
                                "target_label": endpoints[1]["iface_name"],
                            }
                        }
                    )
                elif len(endpoints) > 2:
                    # Add network as node
                    cy_nodes.append(
                        {
                            "data": {
                                "id": f"Link{link['id']}",
                                "label": f"N{link['id']}",
                                "image_url": "/static/icons/l2-switch.svg",
                            },
                        }
                    )
                    for endpoint in endpoints:
                        cy_edges.append(
                            {
                                "data": {
                                    # "id": f"link{link['id']}",
                                    "source": endpoint["node"],
                                    "target": f"Link{link['id']}",
                                    "source_label": endpoint["iface_name"],
                                }
                            }
                        )
            context["elements"] = cy_nodes + cy_edges
        return context


#############################################################################
# Instance
#############################################################################


class LabInstanceQueryMixin:
    """Mixin to encapsulate common Template queryset and permissions logic.

    Used by both UI and API views.
    """

    def get_queryset(self):
        """Return the queryset of `User` objects accessible to the current user.

        - Superusers can access all `User` objects.
        - Staff users can see users who share at least one group
        - Non-superusers can only access their own `User` object.
        """
        qs = Lab.objects.all()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `User` objects
            return qs
        if user.is_staff:
            # Staff users can see users who share at least one group
            groups = user.groups.all()
            return qs.filter(user__groups__in=groups).distinct()
        # Non-admin users can only see their own user
        return qs.filter(user=user)

    def get_object(self):
        """Return a `User` object only if the user has permission.

        - Superusers can access any `User`.
        - Staff users can see users who share at least one group.
        - Non-superusers can only access their own `User` object.

        Raises:
            PermissionDenied: If the user does not have access.
        """
        obj = super().get_object()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `User` objects
            return obj
        if user.is_staff:
            if user.groups.filter(
                pk__in=obj.groups.values_list("pk", flat=True)
            ).exists():
                return obj
        if user == obj:
            # Non-admin users can only see the `Group` objects they belong to
            return obj
        raise PermissionDenied(messages.PERMISSION_DENIED)


class LabInstanceAPIViewSet(LabQueryMixin, APICRUDViewSet):
    """REST API endpoints for Template model."""

    serializer_class = LabInstanceSerializer
    filterset_class = LabInstanceFilter


class LabInstanceBulkDeleteView(LabInstanceQueryMixin, ObjectBulkDeleteView):
    """HTML view for deleting multiple `User` objects at once."""

    model = LabInstance


class LabInstanceChangeView(LabInstanceQueryMixin, ObjectChangeView):
    """HTML view for updating an existing `User`."""

    model = LabInstance
    form_class = LabInstanceForm


class LabInstanceDeleteView(LabInstanceQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single `User`."""

    model = LabInstance


class LabInstanceDetailView(LabInstanceQueryMixin, ObjectDetailView):
    model = LabInstance
    exclude = ["id"]
    sequence = ["name", "created_at", "description"]


class LabInstanceListView(LabInstanceQueryMixin, ObjectListView):
    model = LabInstance
    table_class = LabInstanceTable
    filterset_class = LabInstanceFilter
