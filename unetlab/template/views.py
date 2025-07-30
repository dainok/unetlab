"""Views, called by URLs."""

from django.views.generic import DetailView
from django.conf import settings
from django_filters.views import FilterView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from template.models import NodeTemplate
from template.serializers import NodeTemplateSerializer
from template.filters import NodeTemplateFilter
from django_tables2 import SingleTableView
from template.tables import NodeTemplateTable

# from template.tasks import do_rescan
from unetlab.utils import db_fields_to_dict
from unetlab.views import CommonMixin, BaseListView
from unetlab.permissions import IsAdminOrStaff


class NodeTemplateQueryMixin:
    """Mixin to encapsulate common Template queryset and permissions logic.

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


class NodeTemplateViewSet(
    NodeTemplateQueryMixin,
    mixins.ListModelMixin,  # GET /host/
    mixins.RetrieveModelMixin,  # GET /host/{id}/
    viewsets.GenericViewSet,
):
    """REST API endpoints for Template model."""

    serializer_class = NodeTemplateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NodeTemplateFilter
    queryset = NodeTemplate.objects.all()


class NodeTemplateListView(BaseListView):
    model = NodeTemplate
    table_class = NodeTemplateTable
    template_name = "objects/object_list.html"
    paginate_by = settings.REST_FRAMEWORK["PAGE_SIZE"]
    actions = ["delete"]
    vip_actions = ["Template-rescan"]


class NodeTemplateDetailView(NodeTemplateQueryMixin, CommonMixin, DetailView):
    """HTML detail view for a single template."""

    model = NodeTemplate
    template_name = "objects/host_detail.html"

    def get_context_data(self, **kwargs):
        """Add host field metadata and logs list to context."""
        context = super().get_context_data(**kwargs)
        context["host_fields"] = db_fields_to_dict(NodeTemplate._meta.fields)
        return context
