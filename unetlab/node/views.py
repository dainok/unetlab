"""Views, called by URLs."""

import hashlib
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from node.filters import NodeFilter, NodeTemplateFilter
from node.models import Node, NodeTemplate
from node.serializers import NodeSerializer, NodeTemplateSerializer, UploadDiskSerializer
from node.tables import NodeTable, NodeTemplateTable
from node.forms import NodeForm, NodeTemplateForm
from ui.include.permissions import IsAdmin, IsAdminOrStaff
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
# Nodes
#############################################################################


class NodeQueryMixin:
    """Mixin to encapsulate common Template queryset and permissions logic.

    Used by both UI and API views.
    """


class NodeAPIViewSet(NodeQueryMixin, APICRUDViewSet):
    """REST API endpoints for Template model."""

    serializer_class = NodeSerializer
    filterset_class = NodeFilter

    @action(detail=False, methods=["post"])
    def stop(self, request):
        # do_rescan(username=request.user.username)
        return Response({}, status=status.HTTP_202_ACCEPTED)
    
    @action(detail=False, methods=["post"])
    def start(self, request):
        # do_rescan(username=request.user.username)
        return Response({}, status=status.HTTP_202_ACCEPTED)
    
    @action(detail=False, methods=["post"])
    def wipe(self, request):
        # do_rescan(username=request.user.username)
        return Response({}, status=status.HTTP_202_ACCEPTED)
    

class NodeBulkDeleteView(ObjectBulkDeleteView):
    """HTML view for deleting multiple `Group` objects at once."""

    model = Node
    permission_classes = [IsAdmin]


class NodeChangeView(ObjectChangeView):
    model = Node
    form_class = NodeForm
    permission_classes = [IsAdmin]


class NodeCreateView(ObjectCreateView):
    model = Node
    form_class = NodeForm


class NodeDeleteView(ObjectDeleteView):
    """HTML view for deleting a single `Group`."""

    model = Node
    permission_classes = [IsAdmin]


class NodeDetailView(ObjectDetailView):
    model = Node
    exclude = ["id"]
    sequence = ["name", "created_at", "description"]


class NodeListView(ObjectListView):
    model = Node
    table_class = NodeTable
    filterset_class = NodeFilter


#############################################################################
# Templates
#############################################################################


class NodeTemplateQueryMixin:
    """Mixin to encapsulate common Template queryset and permissions logic.

    Used by both UI and API views.
    """


class NodeTemplateAPIViewSet(NodeTemplateQueryMixin, APICRUDViewSet):
    """REST API endpoints for Template model."""

    serializer_class = NodeTemplateSerializer
    filterset_class = NodeTemplateFilter

    @action(detail=False, methods=["post"])
    def build(self, request):
        # do_rescan(username=request.user.username)
        return Response({}, status=status.HTTP_202_ACCEPTED)
     

class NodeTemplateBulkDeleteView(ObjectBulkDeleteView):
    """HTML view for deleting multiple `Group` objects at once."""

    model = NodeTemplate
    permission_classes = [IsAdmin]


class NodeTemplateChangeView(ObjectChangeView):
    model = NodeTemplate
    form_class = NodeTemplateForm
    permission_classes = [IsAdmin]


class NodeTemplateCreateView(ObjectCreateView):
    model = NodeTemplate
    form_class = NodeTemplateForm


class NodeTemplateDeleteView(ObjectDeleteView):
    """HTML view for deleting a single `Group`."""

    model = NodeTemplate
    permission_classes = [IsAdmin]


class NodeTemplateDetailView(ObjectDetailView):
    model = NodeTemplate
    exclude = ["id"]
    sequence = ["name", "created_at", "description"]


class NodeTemplateListView(ObjectListView):
    model = NodeTemplate
    table_class = NodeTemplateTable
    filterset_class = NodeTemplateFilter


#############################################################################
# Disks
#############################################################################


class DiskTemplateCreateAPIView(APIView):
    """Add disk."""

    permission_classes = [IsAdminOrStaff]

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

        f = serializer.validated_data["file"]
        checksum = hashlib.md5()  # nosec B324 # not used for security
        for chunk in f.chunks():
            checksum.update(chunk)
        f.seek(0)

        disk_filename = f"{template.name}.vma"
        path = default_storage.save(
            f"{template.vendor}-{template.os}/{disk_filename}".lower(), f
        )
        url = default_storage.url(path)

        disk = {"filename": disk_filename, "checksum": checksum.hexdigest(), "url": url}

        # Upload
        # curl -X POST -H "Authorization: Token d94fef88dbd7c4f70cdec97e880ea7b92286bde0" -F "file=@repositories/vyos/vyos/vzdump-qemu-vyos-vyos-2025.07.28-0022.vma" http://localhost:8000/api/template/6/disk
        # Download
        # curl -L -X GET -H "Authorization: Token d94fef88dbd7c4f70cdec97e880ea7b92286bde0" http://localhost:8000/files/vyos-vyos/template-local-vyos-vyos-2025.07.28-0022-unl.vma --output a

        # Aggiorna la lista disks del template (aggiunge il nuovo file)
        template.disk_checksum = checksum.hexdigest()
        template.save()

        return Response({"disk": disk}, status=status.HTTP_201_CREATED)
