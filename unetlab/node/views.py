"""Views, called by URLs."""

from django.views.generic import DetailView
from django.conf import settings
from django_filters.views import FilterView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from node.models import NodeTemplate
from node.serializers import NodeTemplateSerializer
from node.filters import NodeTemplateFilter
from django_tables2 import SingleTableView
from node.tables import NodeTemplateTable
from ui.views import ObjectDetailView, ObjectChangeView, ObjectCreateView
from django.urls import reverse
from node.forms import NodeTemplateForm

# from node.tasks import do_rescan
from unetlab.utils import db_fields_to_dict
from unetlab.views import CommonMixin, BaseListView
from unetlab.permissions import IsAdminOrStaff


class NodeTemplateQueryMixin:
    """Mixin to encapsulate common Template queryset and permissions logic.

    Used by both UI and API views.
    """


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
    filterset_class = NodeTemplateFilter
    actions = ["delete"]
    vip_actions = ["Template-rescan"]


class NodeTemplateDetailView(ObjectDetailView):
    model = NodeTemplate
    exclude=["id"]
    sequence=["name", "created_at", "description"]
    list_view = "template_list"
    # is_enabled = GreenRedBooleanColumn()



class NodeTemplateCreateView(ObjectCreateView):
    model = NodeTemplate
    form_class = NodeTemplateForm
    def get_success_url(self):
        # instance è l'oggetto appena creato
        return reverse('template_detail', kwargs={'pk': self.object.pk})

class NodeTemplateChangeView(ObjectChangeView):
    model = NodeTemplate
    form_class = NodeTemplateForm
    # fields = '__all__'
    # template_name = 'object_form.html'
    # success_url = reverse_lazy('home')