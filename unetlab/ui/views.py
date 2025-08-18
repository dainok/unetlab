"""Views for managing Groups.

This module provides both HTML UI views and REST API endpoints
for the `Group` model, including creation, modification,
retrieval, and deletion.
"""

from django.core.exceptions import PermissionDenied
from django.contrib import messages as django_msgs
from django.contrib.auth.models import Group, User
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from constance import config
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from unetlab.views import CommonMixin
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
from ui.filters import GroupFilter, TokenFilter, UserFilter
from ui.forms import GroupForm, UserForm
from ui.serializers import GroupSerializer, UserSerializer
from ui.tables import GroupTable, TokenTable, UserTable


#############################################################################
# Contance settings
#############################################################################


class ConstanceListView(CommonMixin, TemplateView):
    template_name = "ui/settings_list.html"

    def get_variables(self):
        return {key: getattr(config, key) for key in dir(config)}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["variables"] = self.get_variables()
        return context


class ConstanceUpdateView(CommonMixin, TemplateView):
    template_name = "ui/settings_form.html"

    def get_variables(self):
        # Restituisce tutte le variabili di Constance come dizionario
        return {key: getattr(config, key) for key in dir(config)}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context["variables"] = self.get_variables()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        for key in dir(config):
            if key in request.POST:
                value = request.POST[key]
                default_value = getattr(config, key)
                # Convertiamo il tipo
                if isinstance(default_value, bool):
                    value = value.lower() in ["true", "1", "on"]
                elif isinstance(default_value, int):
                    try:
                        value = int(value)
                    except ValueError:
                        django_msgs.error(request, f"Valore per {key} non valido!")
                        continue
                config._backend.set(key, value)
        django_msgs.success(request, "Configurazioni aggiornate con successo!")
        return redirect("settings_list")


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


class UserQueryMixin:
    """Mixin encapsulating common queryset and permission logic for `User`.

    Used by both HTML views and API views.
    """

    def get_queryset(self):
        """Return the queryset of `User` objects accessible to the current user.

        - Superusers can access all `User` objects.
        - Staff users can see users who share at least one group
        - Non-superusers can only access their own `User` object.
        """
        qs = User.objects.all()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `User` objects
            return qs
        if user.is_staff:
            # Staff users can see users who share at least one group
            groups = user.groups.all()
            return qs.filter(groups__in=groups).distinct()
        # Non-admin users can only see their own user
        return qs.filter(username=user.username)

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
            if obj.is_superuser:
                raise PermissionDenied(messages.PERMISSION_ADMIN)
            # Staff users can see users who share at least one group
            if user.groups.filter(
                pk__in=obj.groups.values_list("pk", flat=True)
            ).exists():
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


class TokenQueryMixin:
    """Mixin encapsulating common queryset and permission logic for `Token`.

    Used by both HTML views and API views.
    """

    def get_queryset(self):
        """Return the queryset of `User` objects accessible to the current user.

        - Superusers can access all `User` objects.
        - Staff users can see users who share at least one group
        - Non-superusers can only access their own `User` object.
        """
        qs = Token.objects.all()
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all `User` objects
            return qs
        if user.is_staff:
            # Staff users can see users who share at least one group
            groups = user.groups.all()
            return qs.filter(user__groups__in=groups, is_superuser=False).distinct()
        # Non-admin users can only see their own user
        return qs.filter(user__username=user.username)

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
            if obj.is_superuser:
                raise PermissionDenied(messages.PERMISSION_ADMIN)
            # Staff users can see users who share at least one group
            if user.groups.filter(
                pk__in=obj.groups.values_list("pk", flat=True)
            ).exists():
                return obj
        if user == obj:
            # Non-admin users can only see the `Group` objects they belong to
            return obj
        raise PermissionDenied(messages.PERMISSION_DENIED)


class TokenBulkDeleteView(ObjectBulkDeleteView):
    """HTML view for deleting multiple `Token` objects at once."""

    model = Token
    permission_classes = [IsAdmin]


class TokenCreateView(ObtainAuthToken):
    """
    API per permettere a ciascun utente di generare il proprio token.
    """

    def post(self, request, *args, **kwargs):
        Token.objects.get_or_create(user=request.user)
        return redirect("token_list")


class TokenDeleteView(ObjectDeleteView):
    """HTML view for deleting a single `Token`."""

    model = Token


class TokenListView(TokenQueryMixin, ObjectListView):
    """HTML view for displaying a table of `Token` objects."""

    filterset_class = TokenFilter
    model = Token
    table_class = TokenTable
