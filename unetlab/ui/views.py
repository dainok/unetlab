"""Views for UI app."""

from constance import config
from django.contrib import messages as django_msgs
from django.contrib.auth.models import Group, User
from django.db.models import Q, query, Prefetch
from django.http import (
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
import django_tables2 as tables
from ui.filters import GroupFilter, TokenFilter, UserFilter
from ui.forms import GroupForm, TokenForm, UserForm
from ui.include.permissions import ObjectPermission
from ui.include.tables import (
    GreenRedBooleanColumn,
    GreenRedReverseBooleanColumn,
    GroupColumn,
    UserColumn,
)
from ui.include.views import (
    APICRUDViewSet,
    ObjectBulkDeleteView,
    ObjectChangeView,
    ObjectCreateView,
    ObjectDeleteView,
    ObjectDetailView,
    ObjectListView,
    TemplateMixin,
)
from ui.permissions import (
    ConstancePermissionPolicy,
    GroupPermissionPolicy,
    HomePermissionPolicy,
    TokenPermissionPolicy,
    UserPermissionPolicy,
)
from ui.serializers import GroupSerializer, UserSerializer
from ui.tables import GroupTable, TokenTable, UserTable


#############################################################################
# Contance settings
#############################################################################


class ConstanceListView(TemplateMixin, TemplateView):
    """View to display Constance settings as a list."""

    policy_class = ConstancePermissionPolicy
    template_name = 'ui/settings_list.html'

    def get_variables(self) -> dict:
        """Retrieve all Constance configuration variables."""

        return {key: getattr(config, key) for key in dir(config)}

    def get_context_data(self, **kwargs) -> dict:
        """Add Constance variables to the template context."""

        context = super().get_context_data(**kwargs)
        context['variables'] = self.get_variables()
        return context


class ConstanceUpdateView(TemplateMixin, TemplateView):
    """View to display and update Constance settings via a form."""

    policy_class = ConstancePermissionPolicy
    template_name = 'ui/settings_form.html'

    def get_variables(self) -> dict:
        """Retrieve all Constance configuration variables."""
        return {key: getattr(config, key) for key in dir(config)}

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Handle GET request and render the settings form with current values."""
        context = self.get_context_data()
        context['variables'] = self.get_variables()
        return render(request, self.template_name, context)

    def post(
        self, request, *args, **kwargs
    ) -> HttpResponsePermanentRedirect | HttpResponseRedirect:
        """Handle POST request to update Constance settings."""
        for key in dir(config):
            if key in request.POST:
                value = request.POST[key]
                default_value = getattr(config, key)
                # Convert type to match default
                if isinstance(default_value, bool):
                    value = value.lower() in ['true', '1', 'on']
                elif isinstance(default_value, int):
                    try:
                        value = int(value)
                    except ValueError:
                        django_msgs.error(
                            request, _('Value error (%(key)s) .') % {'key': key}
                        )
                        continue
                config._backend.set(key, value)
        django_msgs.success(request, _('Configuration updated.'))
        return redirect('settings_list')


#############################################################################
# Group
#############################################################################


class GroupQueryMixin:
    """Mixin encapsulating common queryset and permission logic for Group objects."""

    filterset_class = GroupFilter
    form_class = GroupForm
    model = Group
    policy_class = GroupPermissionPolicy
    serializer_class = GroupSerializer
    table_class = GroupTable

    def get_queryset(self) -> query.QuerySet:
        """Return the queryset of Group objects accessible to the current user."""
        users_prefetch = Prefetch(
            'user_set', queryset=User.objects.all().order_by('username')
        )
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all Group objects
            # order_by is required to aboid UnorderedObjectListWarning warning
            return Group.objects.all().order_by('name').prefetch_related(users_prefetch)
        # Non-admin users can only see the Group objects they belong to
        # order_by is required to aboid UnorderedObjectListWarning warning
        return user.groups.all().order_by('name').prefetch_related(users_prefetch)


class GroupAPIViewSet(GroupQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the Group model."""

    pass


class GroupBulkDeleteView(GroupQueryMixin, ObjectBulkDeleteView):
    """HTML view for deleting multiple Group objects at once."""

    pass


class GroupChangeView(GroupQueryMixin, ObjectChangeView):
    """HTML view for updating an existing Group."""

    pass


class GroupCreateView(GroupQueryMixin, ObjectCreateView):
    """HTML view for creating a new Group."""

    pass


class GroupDeleteView(GroupQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single Group."""

    pass


class GroupDetailView(GroupQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a Group."""

    users = UserColumn()

    exclude = ['id']
    sequence = ['name', 'users']


class GroupListView(GroupQueryMixin, ObjectListView):
    """HTML view for displaying a table of Group objects."""

    pass


#############################################################################
# User
#############################################################################


class UserQueryMixin:
    """Mixin encapsulating common queryset and permission logic for User objects."""

    filterset_class = UserFilter
    form_class = UserForm
    model = User
    policy_class = UserPermissionPolicy
    serializer_class = UserSerializer
    table_class = UserTable

    def get_queryset(self) -> query.QuerySet:
        """Return the queryset of User objects accessible to the current user."""
        groups_prefetch = Prefetch(
            'groups', queryset=Group.objects.all().order_by('name')
        )
        # order_by is required to aboid UnorderedObjectListWarning warning
        qs = User.objects.all().order_by('username').prefetch_related(groups_prefetch)
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all User objects
            return qs
        # Staff and standard users can see users who share at least one group
        groups = user.groups.all()
        return qs.filter(Q(groups__in=groups) | Q(id=user.id)).distinct()


class UserAPIViewSet(UserQueryMixin, APICRUDViewSet):
    """REST API ViewSet for the User model."""

    pass


class UserBulkDeleteView(UserQueryMixin, ObjectBulkDeleteView):
    """HTML view for deleting multiple User objects at once."""

    pass


class UserChangeView(UserQueryMixin, ObjectChangeView):
    """HTML view for updating an existing User."""

    pass


class UserCreateView(UserQueryMixin, ObjectCreateView):
    """HTML view for creating a new User."""

    pass


class UserDeleteView(UserQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single User."""

    pass


class UserDetailView(UserQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a User."""

    date_joined = tables.DateColumn(orderable=True, format='Y-m-d')
    groups = GroupColumn()
    is_active = GreenRedBooleanColumn()
    is_staff = GreenRedReverseBooleanColumn(verbose_name='Staff')
    is_superuser = GreenRedReverseBooleanColumn(verbose_name='Admin')
    last_login = tables.DateColumn(orderable=True, format='Y-m-d H:i')

    exclude = ('id', 'password')
    sequence = (
        'username',
        'first_name',
        'last_name',
        'email',
        'is_active',
        'is_superuser',
        'is_staff',
        'groups',
        'date_joined',
        'last_login',
    )


class UserListView(UserQueryMixin, ObjectListView):
    """HTML view for displaying a table of User objects."""

    pass


#############################################################################
# Token
#############################################################################


class TokenQueryMixin:
    """Mixin encapsulating common queryset and permission logic for Token objects."""

    filterset_class = TokenFilter
    form_class = TokenForm
    model = Token
    policy_class = TokenPermissionPolicy
    serializer_class = None
    table_class = TokenTable

    def get_queryset(self) -> query.QuerySet:
        """Return the queryset of Token objects accessible to the current user."""
        # order_by is required to aboid UnorderedObjectListWarning warning
        qs = Token.objects.all().order_by('user__username')
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all Token objects
            return qs
        # Staff and standard users can only see their own Token
        return qs.filter(user__username=user.username)


class TokenBulkDeleteView(TokenQueryMixin, ObjectBulkDeleteView):
    """HTML view for deleting multiple Token objects at once."""

    pass


class TokenCreateView(TokenQueryMixin, ObtainAuthToken):
    """HTML view for creating a new Token."""

    permission_classes = [ObjectPermission]

    def post(
        self, request, *args, **kwargs
    ) -> HttpResponsePermanentRedirect | HttpResponseRedirect:
        """Create one Token per User."""
        Token.objects.get_or_create(user=request.user)
        return redirect('token_list')


class TokenDeleteView(TokenQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single Token."""

    pass


class TokenListView(TokenQueryMixin, ObjectListView):
    """HTML view for displaying a table of Token objects."""

    pass


#############################################################################
# Home
#############################################################################


class HomeView(TemplateMixin, TemplateView):
    """Render the home page."""

    policy_class = HomePermissionPolicy
    template_name = 'ui/home.html'
