"""Views, called by URLs."""

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from proxmox.models import ProxmoxHost
from proxmox.serializers import ProxmoxHostSerializer
from proxmox.filters import ProxmoxHostFilter
from proxmox.tables import ProxmoxHostTable
from proxmox.tasks import do_rescan
from ui.include.permissions import IsAdminOrStaff
from ui.include.views import (
    APIRViewSet,
    ObjectDetailView,
    ObjectListView,
)


class ProxmoxHostQueryMixin:
    """Mixin to encapsulate common ProxmoxHost queryset and permissions logic.

    Used by both UI and API views.
    """

    queryset = ProxmoxHost.objects.all()


class ProxmoxHostAPIViewSet(ProxmoxHostQueryMixin, APIRViewSet):
    """REST API endpoints for ProxmoxHost model."""

    serializer_class = ProxmoxHostSerializer
    filterset_class = ProxmoxHostFilter

    @action(detail=False, methods=["post"])
    def rescan(self, request):
        do_rescan(username=request.user.username)
        return Response({}, status=status.HTTP_202_ACCEPTED)


class ProxmoxHostDetailView(ProxmoxHostQueryMixin, ObjectDetailView):
    """HTML detail view for a single ProxmoxHost."""

    model = ProxmoxHost


class ProxmoxHostListView(ProxmoxHostQueryMixin, ObjectListView):
    filterset_class = ProxmoxHostFilter
    model = ProxmoxHost
    table_class = ProxmoxHostTable
