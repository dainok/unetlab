"""Views, called by URLs."""

from rest_framework.response import Response
from rest_framework.views import APIView
from repository.models import Repository
from repository.serializers import RepositorySerializer
from repository.filters import RepositoryFilter
from repository.forms import RepositoryForm
from repository.tables import RepositoryTable
from repository.tasks import do_rescan
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


class RepositoryQueryMixin:
    """Mixin encapsulating common queryset and permission logic for `Group`.

    Used by both HTML views and API views.
    """

    queryset = Repository.objects.all()


class RepositoryAPIViewSet(RepositoryQueryMixin, APICRUDViewSet):
    """REST API endpoints for Repository model."""

    serializer_class = RepositorySerializer
    filterset_class = RepositoryFilter


class RepositoryBulkDeleteView(ObjectBulkDeleteView):
    """HTML view for deleting multiple `User` objects at once."""

    model = Repository
    permission_classes = [IsAdmin]


class RepositoryChangeView(ObjectChangeView):
    """HTML view for updating an existing `User`."""

    model = Repository
    form_class = RepositoryForm
    permission_classes = [IsAdmin]


class RepositoryCreateView(ObjectCreateView):
    """HTML view for creating a new `User`."""

    model = Repository
    form_class = RepositoryForm
    permission_classes = [IsAdmin]


class RepositoryDeleteView(ObjectDeleteView):
    """HTML view for deleting a single `User`."""

    model = Repository
    permission_classes = [IsAdmin]
    exclude = ["id"]
    sequence = ["name", "created_at", "description"]


class RepositoryDetailView(RepositoryQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a `User`."""

    model = Repository
    # exclude = ["id", "password"]
    # sequence = [
    #     "username",
    #     "first_name",
    #     "last_name",
    #     "email",
    #     "is_active",
    #     "is_superuser",
    #     "is_staff",
    # ]


class RepositoryListView(RepositoryQueryMixin, ObjectListView):
    """HTML view for displaying a table of `User` objects."""

    filterset_class = RepositoryFilter
    model = Repository
    table_class = RepositoryTable


class RepositoryRescanAPIView(APIView):
    """Manage rescan action."""

    permission_classes = [IsAdminOrStaff]

    def post(self, request):
        do_rescan(username=request.user.username)
        # TODO: review data model
        return Response({"status": "rescan triggered"})
