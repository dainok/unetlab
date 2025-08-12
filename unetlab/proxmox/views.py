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
from ui.views import ObjectDetailView


class ProxmoxHostQueryMixin:
    """Mixin to encapsulate common ProxmoxHost queryset and permissions logic.

    Used by both UI and API views.
    """


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
    filterset_class = ProxmoxHostFilter
    list_view = "host_list"


class ProxmoxHostDetailView(ObjectDetailView):
    """HTML detail view for a single ProxmoxHost."""

    model = ProxmoxHost
    list_view = "host_list"
    # exclude=["id"]
    # sequence=["name", "created_at", "description"]


class ProxmoxRescanView(APIView):
    """Manage rescan action."""

    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def post(self, request):
        do_rescan(username=request.user.username)
        return Response({"status": "rescan triggered"})
