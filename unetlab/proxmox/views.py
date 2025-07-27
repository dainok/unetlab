"""Views, called by URLs."""

from django.views.generic import DetailView
from django.conf import settings
from django_filters.views import FilterView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from proxmox.models import ProxmoxHost
from proxmox.serializers import ProxmoxHostSerializer
from proxmox.filters import ProxmoxHostFilter
from django_tables2 import SingleTableView
from proxmox.tables import ProxmoxHostTable
from proxmox.tasks import do_rescan
from unetlab.utils import db_fields_to_dict
from unetlab.views import CommonMixin, BaseListView
from unetlab.permissions import IsAdminOrStaff


class ProxmoxHostQueryMixin:
    """Mixin to encapsulate common ProxmoxHost queryset and permissions logic.

    Used by both UI and API views.
    """

    def get_paginate_by(self, queryset):
        """Allow client to customize pagination via 'per_page' query param.

        Enforces a maximum of 100 per page; defaults to 10.
        """
        per_page = self.request.GET.get("per_page")
        try:
            per_page = int(per_page)
            if per_page > 100:
                return 100
            if per_page > 0:
                return per_page
        except (TypeError, ValueError):
            pass
        return settings.REST_FRAMEWORK["PAGE_SIZE"]


class ProxmoxHostViewSet(
    ProxmoxHostQueryMixin,
    mixins.ListModelMixin,  # GET /host/
    mixins.RetrieveModelMixin,  # GET /host/{id}/
    viewsets.GenericViewSet,
):
    """REST API endpoints for ProxmoxHost model."""

    serializer_class = ProxmoxHostSerializer
    filterset_class = ProxmoxHostFilter
    filter_backends = [DjangoFilterBackend]
    queryset = ProxmoxHost.objects.all()


class ProxmoxHostListView(BaseListView):
    model = ProxmoxHost
    table_class = ProxmoxHostTable
    template_name = "objects/object_list.html"
    paginate_by = settings.REST_FRAMEWORK["PAGE_SIZE"]
    actions = ["delete"]
    vip_actions = ["host-rescan"]


class ProxmoxHostDetailView(ProxmoxHostQueryMixin, CommonMixin, DetailView):
    """HTML detail view for a single ProxmoxHost."""

    model = ProxmoxHost
    template_name = "objects/host_detail.html"

    def get_context_data(self, **kwargs):
        """Add host field metadata and logs list to context."""
        context = super().get_context_data(**kwargs)
        context["host_fields"] = db_fields_to_dict(ProxmoxHost._meta.fields)
        return context


class ProxmoxRescanView(APIView):
    """Manage rescan action."""

    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def post(self, request):
        do_rescan(username=request.user.username)
        return Response({"status": "rescan triggered"})
