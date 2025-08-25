"""Views, called by URLs."""

from django.core.exceptions import PermissionDenied
from lab.models import Lab, LabInstance
from lab.serializers import LabSerializer, LabInstanceSerializer
from lab.filters import LabFilter, LabInstanceFilter
from lab.forms import LabForm, LabInstanceForm
from lab.tables import LabTable, LabInstanceTable
from ui.include import messages
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
# Lab
#############################################################################


class LabQueryMixin:
    """Mixin to encapsulate common Template queryset and permissions logic.

    Used by both UI and API views.
    """

    def get_queryset(self):
        """Return the queryset of `User` objects accessible to the current user.

        - Superusers can access all `User` objects.
        - Staff users can see users who share at least one group
        - Non-superusers can only access their own `User` object.
        """
        qs = Lab.objects.all()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `User` objects
            return qs
        if user.is_staff:
            # Staff users can see users who share at least one group
            groups = user.groups.all()
            return qs.filter(user__groups__in=groups).distinct()
        # Non-admin users can only see their own user
        return qs.filter(user=user)

    def get_object(self):
        """Return a `User` object only if the user has permission.

        - Superusers can access any `User`.
        - Staff users can see users who share at least one group.
        - Non-superusers can only access their own `User` object.

        Raises:
            PermissionDenied: If the user does not have access.
        """
        obj = super().get_object()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `User` objects
            return obj
        if user.is_staff:
            if user.groups.filter(
                pk__in=obj.groups.values_list("pk", flat=True)
            ).exists():
                return obj
        if user == obj:
            # Non-admin users can only see the `Group` objects they belong to
            return obj
        raise PermissionDenied(messages.PERMISSION_DENIED)


class LabAPIViewSet(LabQueryMixin, APICRUDViewSet):
    """REST API endpoints for Template model."""

    serializer_class = LabSerializer
    filterset_class = LabFilter


class LabBulkDeleteView(ObjectBulkDeleteView):
    """HTML view for deleting multiple `User` objects at once."""

    model = Lab


class LabChangeView(ObjectChangeView):
    """HTML view for updating an existing `User`."""

    model = Lab
    form_class = LabForm


class LabCreateView(ObjectCreateView):
    """HTML view for creating a new `User`."""

    model = Lab
    form_class = LabForm


class LabDeleteView(ObjectDeleteView):
    """HTML view for deleting a single `User`."""

    model = Lab


class LabDetailView(ObjectDetailView):
    model = Lab
    exclude = ["id"]
    sequence = ["name", "created_at", "description"]


class LabListView(ObjectListView):
    model = Lab
    table_class = LabTable
    filterset_class = LabFilter


#############################################################################
# Instance
#############################################################################


class LabInstanceQueryMixin:
    """Mixin to encapsulate common Template queryset and permissions logic.

    Used by both UI and API views.
    """

    def get_queryset(self):
        """Return the queryset of `User` objects accessible to the current user.

        - Superusers can access all `User` objects.
        - Staff users can see users who share at least one group
        - Non-superusers can only access their own `User` object.
        """
        qs = Lab.objects.all()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `User` objects
            return qs
        if user.is_staff:
            # Staff users can see users who share at least one group
            groups = user.groups.all()
            return qs.filter(user__groups__in=groups).distinct()
        # Non-admin users can only see their own user
        return qs.filter(user=user)

    def get_object(self):
        """Return a `User` object only if the user has permission.

        - Superusers can access any `User`.
        - Staff users can see users who share at least one group.
        - Non-superusers can only access their own `User` object.

        Raises:
            PermissionDenied: If the user does not have access.
        """
        obj = super().get_object()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `User` objects
            return obj
        if user.is_staff:
            if user.groups.filter(
                pk__in=obj.groups.values_list("pk", flat=True)
            ).exists():
                return obj
        if user == obj:
            # Non-admin users can only see the `Group` objects they belong to
            return obj
        raise PermissionDenied(messages.PERMISSION_DENIED)


class LabInstanceAPIViewSet(LabQueryMixin, APICRUDViewSet):
    """REST API endpoints for Template model."""

    serializer_class = LabInstanceSerializer
    filterset_class = LabInstanceFilter


class LabInstanceBulkDeleteView(ObjectBulkDeleteView):
    """HTML view for deleting multiple `User` objects at once."""

    model = LabInstance


class LabInstanceChangeView(ObjectChangeView):
    """HTML view for updating an existing `User`."""

    model = LabInstance
    form_class = LabInstanceForm


class LabInstanceDeleteView(ObjectDeleteView):
    """HTML view for deleting a single `User`."""

    model = LabInstance


class LabInstanceDetailView(ObjectDetailView):
    model = LabInstance
    exclude = ["id"]
    sequence = ["name", "created_at", "description"]


class LabInstanceListView(ObjectListView):
    model = LabInstance
    table_class = LabInstanceTable
    filterset_class = LabInstanceFilter
