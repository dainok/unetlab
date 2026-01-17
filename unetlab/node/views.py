"""Views for Node app."""

from django.db.models import query
import django_tables2 as tables
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from node.permissions import NodeTemplatePermissionPolicy
from node.filters import NodeTemplateFilter
from node.models import NodeTemplate
from node.serializers import (
    # NodeSerializer,
    NodeTemplateSerializer,
    # DiskTemplateSerializer,
)
from node.tables import NodeTemplateTable
from node.forms import NodeTemplateForm

# from ui.include.permissions import IsAdmin, IsAdminOrStaff
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


# class NodeQueryMixin:
#     """Mixin to encapsulate common Template queryset and permissions logic.

#     Used by both UI and API views.
#     """


# class NodeAPIViewSet(NodeQueryMixin, APICRUDViewSet):
#     """REST API endpoints for Template model."""

#     serializer_class = NodeSerializer
#     filterset_class = NodeFilter

#     @action(detail=False, methods=['post'])
#     def stop(self, request):
#         # do_rescan(username=request.user.username)
#         return Response({}, status=status.HTTP_202_ACCEPTED)

#     @action(detail=False, methods=['post'])
#     def start(self, request):
#         # do_rescan(username=request.user.username)
#         return Response({}, status=status.HTTP_202_ACCEPTED)

#     @action(detail=False, methods=['post'])
#     def wipe(self, request):
#         # do_rescan(username=request.user.username)
#         return Response({}, status=status.HTTP_202_ACCEPTED)


# class NodeBulkDeleteView(ObjectBulkDeleteView):
#     """HTML view for deleting multiple `Group` objects at once."""

#     model = Node
#     permission_classes = [IsAdmin]


# class NodeChangeView(ObjectChangeView):
#     model = Node
#     form_class = NodeForm
#     permission_classes = [IsAdmin]


# class NodeCreateView(ObjectCreateView):
#     model = Node
#     form_class = NodeForm


# class NodeDeleteView(ObjectDeleteView):
#     """HTML view for deleting a single `Group`."""

#     model = Node
#     permission_classes = [IsAdmin]


# class NodeDetailView(ObjectDetailView):
#     model = Node
#     exclude = ['id']
#     sequence = ['name', 'created_at', 'description']


# class NodeListView(ObjectListView):
#     model = Node
#     table_class = NodeTable
#     filterset_class = NodeFilter


#############################################################################
# Node Templates
#############################################################################


class NodeTemplateQueryMixin:
    """Mixin encapsulating common queryset and permission logic for NodeTemplate objects."""

    filterset_class = NodeTemplateFilter
    form_class = NodeTemplateForm
    model = NodeTemplate
    policy_class = NodeTemplatePermissionPolicy
    serializer_class = NodeTemplateSerializer
    table_class = NodeTemplateTable

    def get_queryset(self) -> query.QuerySet:
        """Return the queryset of NodeTemplate objects accessible to the current user."""
        qs = NodeTemplate.objects.all()
        return qs


class NodeTemplateAPIViewSet(NodeTemplateQueryMixin, APICRUDViewSet):
    """REST API endpoints for NodeTemplate model."""

    @action(detail=False, methods=['post'])
    def rescan(self, request):
        # do_rescan(username=request.user.username)
        return Response({}, status=status.HTTP_202_ACCEPTED)


class NodeTemplateBulkDeleteView(NodeTemplateQueryMixin, ObjectBulkDeleteView):
    """HTML view for deleting multiple NodeTemplate objects at once."""

    pass


class NodeTemplateChangeView(NodeTemplateQueryMixin, ObjectChangeView):
    """HTML view for updating an existing NodeTemplate."""

    pass


class NodeTemplateCreateView(NodeTemplateQueryMixin, ObjectCreateView):
    """HTML view for creating a new NodeTemplate."""

    pass


class NodeTemplateDeleteView(NodeTemplateQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single NodeTemplate."""

    pass


class NodeTemplateDetailView(NodeTemplateQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a NodeTemplate."""

    created = tables.DateColumn(orderable=True, format='Y-m-d')
    updated = tables.DateColumn(orderable=True, format='Y-m-d H:i')

    exclude = ['id']
    sequence = ['name', 'created']


class NodeTemplateListView(NodeTemplateQueryMixin, ObjectListView):
    """HTML view for displaying a table of NodeTemplate objects."""

    pass


#############################################################################
# Disks
#############################################################################


# class DiskTemplateAPIViewSet(viewsets.GenericViewSet):
#     """Add disk."""

#     permission_classes = [IsAdminOrStaff]

#     def create(self, request, template_pk):
#         template = NodeTemplate.objects.filter(pk=template_pk).first()
#         # TODO
#         # if not template:
#         #     return Response({"detail": "Template non trovato"}, status=status.HTTP_404_NOT_FOUND)
#         # return Response({"status": "rescan triggered"})

#         serializer = DiskTemplateSerializer(data=request.data)
#         # TODO
#         serializer.is_valid()
#         # if not serializer.is_valid():
#         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         f = serializer.validated_data['file']
#         checksum = hashlib.md5()  # nosec B324 # not used for security
#         for chunk in f.chunks():
#             checksum.update(chunk)
#         f.seek(0)

#         disk_filename = f'{template.name}.vma'
#         path = default_storage.save(
#             f'{template.vendor}-{template.os}/{disk_filename}'.lower(), f
#         )
#         url = default_storage.url(path)

#         disk = {'filename': disk_filename, 'checksum': checksum.hexdigest(), 'url': url}

#         # Upload
#         # curl -X POST -H "Authorization: Token c3ba14c234d1f079601e27ee953db87c1a724d17" -F "file=@repositories/vyos/vyos/vzdump-qemu-vyos-vyos-2025.07.28-0022.vma" http://localhost:8000/api/template/6/disk/
#         # Download
#         # curl -L -X GET -H "Authorization: Token c3ba14c234d1f079601e27ee953db87c1a724d17" http://localhost:8000/files/vyos-vyos/template-local-vyos-vyos-2025.07.28-0022-unl.vma --output a

#         # Aggiorna la lista disks del template (aggiunge il nuovo file)
#         template.disk_checksum = checksum.hexdigest()
#         template.save()

#         return Response({'disk': disk}, status=status.HTTP_201_CREATED)

#     def destroy(self, request, template_pk=None, checksum=None):
#         """
#         Elimina un disco specifico associato al template.
#         pk = ID del disco
#         """
#         template = get_object_or_404(NodeTemplate, pk=template_pk)
#         disk = get_object_or_404(template.disks, pk=pk)  # assuming related_name='disks'
#         disk.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
