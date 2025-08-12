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
from django import forms
from django.views.generic.edit import UpdateView, CreateView
from repository.tables import RepositoryTable
from repository.tasks import do_rescan
from repository.filters import RepositoryFilter
from unetlab.utils import db_fields_to_dict
from unetlab.views import CommonMixin, BaseListView
from unetlab.permissions import IsAdminOrStaff
from ui.views import ObjectDetailView
from ui.tables import GreenRedBooleanColumn


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
    filterset_class = RepositoryFilter
    actions = ["delete"]
    vip_actions = ["repository-rescan"]


class RepositoryDetailView(ObjectDetailView):
    model = Repository
    exclude = ["id"]
    sequence = ["name", "created_at", "description"]
    # is_enabled = GreenRedBooleanColumn()


class RepositoriesRescanAPIView(APIView):
    """Manage rescan action."""

    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def post(self, request):
        do_rescan(username=request.user.username)
        return Response({"status": "rescan triggered"})
