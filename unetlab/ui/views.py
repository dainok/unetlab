"""Views for managing Groups.

This module provides both HTML UI views and REST API endpoints
for the `Group` model, including creation, modification,
retrieval, and deletion.
"""

from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.edit import FormView
from rest_framework.authtoken.models import Token
from ui.include import messages
from ui.include.permissions import IsAdmin
from ui.include.views import (
    APICRUDViewSet,
    ObjectBulkDeleteView,
    ObjectChangeView,
    ObjectCreateView,
    ObjectDeleteView,
    ObjectDetailView,
    ObjectListView,
)
from ui.filters import GroupFilter, UserFilter
from ui.forms import GroupForm, TokenForm, UserForm
from ui.serializers import GroupSerializer, UserSerializer
from ui.tables import GroupTable, TokenTable, UserTable
from unetlab.views import CommonMixin
from job.models import Job
from job.utils import log


#############################################################################
# Group
#############################################################################


class GroupQueryMixin:
    """Mixin encapsulating common queryset and permission logic for `Group`.

    Used by both HTML views and API views.
    """

    def get_queryset(self):
        """Return the queryset of `Group` objects accessible to the current user.

        - Superusers can access all `Group` objects.
        - Non-superusers can only access `Group` objects they belong to.
        """
        qs = Group.objects.all()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `Group` objects
            return qs
        # Non-admin users can only see the `Group` objects they belong to
        return qs.filter(user=user)

    def get_object(self):
        """Return a `Group` object only if the user has permission.

        - Superusers can access any `Group`.
        - Non-superusers can only access `Group` objects they belong to.

        Raises:
            PermissionDenied: If the user does not have access.
        """
        obj = super().get_object()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `Group` objects
            return obj
        if user in obj.user_set.all():
            # Non-admin users can only see the `Group` objects they belong to
            return obj
        raise PermissionDenied(messages.PERMISSION_DENIED)


class GroupAPIViewSet(GroupQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the `Group` model."""

    serializer_class = GroupSerializer
    filterset_class = GroupFilter


class GroupBulkDeleteView(ObjectBulkDeleteView):
    """HTML view for deleting multiple `Group` objects at once."""

    model = Group
    permission_classes = [IsAdmin]


class GroupChangeView(ObjectChangeView):
    """HTML view for updating an existing `Group`."""

    model = Group
    form_class = GroupForm
    permission_classes = [IsAdmin]


class GroupCreateView(ObjectCreateView):
    """HTML view for creating a new `Group`."""

    model = Group
    form_class = GroupForm
    permission_classes = [IsAdmin]


class GroupDeleteView(ObjectDeleteView):
    """HTML view for deleting a single `Group`."""

    model = Group
    permission_classes = [IsAdmin]


class GroupDetailView(GroupQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a `Group`."""

    model = Group
    exclude = ["id"]


class GroupListView(GroupQueryMixin, ObjectListView):
    """HTML view for displaying a table of `Group` objects."""

    filterset_class = GroupFilter
    model = Group
    table_class = GroupTable


#############################################################################
# User
#############################################################################
UserFields = [
    "username",
    "first_name",
    "last_name",
    "email",
    "is_active",
    "is_superuser",
    "is_staff",
    "groups",
]


class UserQueryMixin:
    """Mixin encapsulating common queryset and permission logic for `User`.

    Used by both HTML views and API views.
    """

    def get_queryset(self):
        """Return the queryset of `User` objects accessible to the current user.

        - Superusers can access all `User` objects.
        - Non-superusers can only access their own `User` object.
        """
        qs = User.objects.all()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `User` objects
            return qs
        # Non-admin users can only see their own user
        return qs.filter(username=user.username)

    def get_object(self):
        """Return a `User` object only if the user has permission.

        - Superusers can access any `User`.
        - Non-superusers can only access their own `User` object.

        Raises:
            PermissionDenied: If the user does not have access.
        """
        obj = super().get_object()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `User` objects
            return obj
        if user == obj:
            # Non-admin users can only see the `Group` objects they belong to
            return obj
        raise PermissionDenied(messages.PERMISSION_DENIED)


class UserAPIViewSet(UserQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the `User` model."""

    serializer_class = UserSerializer
    filterset_class = UserFilter


class UserBulkDeleteView(ObjectBulkDeleteView):
    """HTML view for deleting multiple `User` objects at once."""

    model = User
    permission_classes = [IsAdmin]


class UserChangeView(ObjectChangeView):
    """HTML view for updating an existing `User`."""

    model = User
    form_class = UserForm
    permission_classes = [IsAdmin]


class UserCreateView(ObjectCreateView):
    """HTML view for creating a new `User`."""

    model = User
    form_class = UserForm
    permission_classes = [IsAdmin]


class UserDeleteView(ObjectDeleteView):
    """HTML view for deleting a single `User`."""

    model = User
    permission_classes = [IsAdmin]


class UserDetailView(UserQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a `User`."""

    model = User
    exclude = ["id", "password"]
    sequence = [
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_superuser",
        "is_staff",
    ]


class UserListView(UserQueryMixin, ObjectListView):
    """HTML view for displaying a table of `User` objects."""

    filterset_class = UserFilter
    model = User
    table_class = UserTable


#############################################################################
# Token
#############################################################################


# class TokenListView(BaseListView):
#     model = Token
#     table_class = TokenTable
#     # filterset_class = ProxmoxHostFilter
#     list_view = "token_list"


# class TokenDetailView(ObjectDetailView):
#     """HTML detail view for a single ProxmoxHost."""

#     model = Token
#     list_view = "token_detail"
#     # exclude=["id"]
#     # sequence=["name", "created_at", "description"]
