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
from node.models import NodeTemplate
from node.serializers import NodeTemplateSerializer, UploadDiskSerializer
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



class DiskTemplateCreateAPIView(APIView):
    """Add disk."""

    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def post(self, request, pk):
        template = NodeTemplate.objects.filter(pk=pk).first()
        # TODO
        # if not template:
        #     return Response({"detail": "Template non trovato"}, status=status.HTTP_404_NOT_FOUND)
            # return Response({"status": "rescan triggered"})

        serializer = UploadDiskSerializer(data=request.data)
        # TODO
        serializer.is_valid()
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        f = serializer.validated_data['file']
        checksum = hashlib.md5()
        for chunk in f.chunks():
            checksum.update(chunk)
        f.seek(0)

        disk_filename = f"{template.name}.vma"
        path = default_storage.save(f'{template.vendor}-{template.os}/{disk_filename}'.lower(), f)
        url = default_storage.url(path)

        disk = {
            "filename": disk_filename,
            "checksum": checksum.hexdigest(),
            "url": url
        }

        # Aggiorna la lista disks del template (aggiunge il nuovo file)
        template.disk_checksum = checksum.hexdigest()
        template.save()

        return Response({"disk": disk}, status=status.HTTP_201_CREATED)



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
    

class NodeTemplateChangeView(ObjectChangeView):
    model = NodeTemplate
    form_class = NodeTemplateForm
    # fields = '__all__'
    # template_name = 'object_form.html'
    # success_url = reverse_lazy('home')