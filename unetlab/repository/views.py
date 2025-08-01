"""Views, called by URLs."""

from django.views.generic import DetailView
from django.conf import settings
from django_filters.views import FilterView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from repository.models import Repository
from repository.serializers import RepositorySerializer
from django_tables2 import SingleTableView
from repository.tables import RepositoryTable
from repository.tasks import do_rescan
from unetlab.utils import db_fields_to_dict
from unetlab.views import CommonMixin, BaseListView
from unetlab.permissions import IsAdminOrStaff


class RepositoryQueryMixin:
    """Mixin to encapsulate common Repository queryset and permissions logic.

    Used by both UI and API views.
    """


class RepositoryViewSet(
    RepositoryQueryMixin,
    mixins.ListModelMixin,  # GET /host/
    mixins.RetrieveModelMixin,  # GET /host/{id}/
    viewsets.GenericViewSet,
):
    """REST API endpoints for Repository model."""

    serializer_class = RepositorySerializer
    filter_backends = [DjangoFilterBackend]
    queryset = Repository.objects.all()


class RepositoryListView(BaseListView):
    model = Repository
    table_class = RepositoryTable
    actions = ["delete"]
    vip_actions = ["repository-rescan"]


class RepositoryDetailView(RepositoryQueryMixin, CommonMixin, DetailView):
    """HTML detail view for a single Repository."""

    model = Repository
    template_name = "objects/host_detail.html"

    def get_context_data(self, **kwargs):
        """Add host field metadata and logs list to context."""
        context = super().get_context_data(**kwargs)
        context["host_fields"] = db_fields_to_dict(Repository._meta.fields)
        return context


class RepositoriesRescanView(APIView):
    """Manage rescan action."""

    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def post(self, request):
        do_rescan(username=request.user.username)
        return Response({"status": "rescan triggered"})
