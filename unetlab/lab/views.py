"""Views, called by URLs."""

import hashlib
from django.views.generic import DetailView
from django.conf import settings
from django_filters.views import FilterView
from django.core.files.storage import default_storage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from lab.models import Lab
from node.serializers import LabSerializer, UploadDiskSerializer
from node.filters import LabFilter
from django_tables2 import SingleTableView
from node.tables import LabTable
from ui.views import ObjectDetailView, ObjectChangeView, ObjectCreateView
from django.urls import reverse
from node.forms import LabForm

# from node.tasks import do_rescan
from unetlab.utils import db_fields_to_dict
from unetlab.views import CommonMixin, BaseListView
from unetlab.permissions import IsAdminOrStaff


class LabQueryMixin:
    """Mixin to encapsulate common Template queryset and permissions logic.

    Used by both UI and API views.
    """


class LabViewSet(
    LabQueryMixin,
    mixins.ListModelMixin,  # GET /host/
    mixins.RetrieveModelMixin,  # GET /host/{id}/
    viewsets.GenericViewSet,
):
    """REST API endpoints for Template model."""

    serializer_class = LabSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = LabFilter
    queryset = Lab.objects.all()



class LabListView(BaseListView):
    model = Lab
    table_class = LabTable
    filterset_class = LabFilter
    actions = ["delete"]
    vip_actions = ["Template-rescan"]


class LabDetailView(ObjectDetailView):
    model = Lab
    exclude=["id"]
    sequence=["name", "created_at", "description"]
    list_view = "template_list"
    # is_enabled = GreenRedBooleanColumn()



class LabCreateView(ObjectCreateView):
    model = Lab
    form_class = LabForm
    # attrs = {
    #     # "title": messages.TABLE_TEMPLATE_TITLE,
    #     # "description": messages.TABLE_TEMPLATE_DESCRIPTION,
    #     "actions": [
    #         {
    #             "action": "Add disk",
    #             "view": "template_disk",
    #         },
    #     ],
    # }
    def get_success_url(self):
        # instance è l'oggetto appena creato
        return reverse('template_detail', kwargs={'pk': self.object.pk})
    

class LabChangeView(ObjectChangeView):
    model = Lab
    form_class = LabForm
    # fields = '__all__'
    # template_name = 'object_form.html'
    # success_url = reverse_lazy('home')