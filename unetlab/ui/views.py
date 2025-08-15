from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group, User
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, permissions
from django_filters.views import FilterView
from django_filters.rest_framework import DjangoFilterBackend
from django_tables2 import SingleTableView
from django_tables2.columns import Column
from ui.include.views import ObjectListView, ObjectDetailView, ObjectCreateView, ObjectChangeView
from ui.filters import GroupFilter
from ui.forms import GroupForm, TokenForm, UserForm
from ui.serializers import UserSerializer
from ui.tables import GroupTable, TokenTable, UserTable
from unetlab.views import CommonMixin, BaseListView, LogListMixin



class UserQueryMixin:
    """Mixin to encapsulate common Job queryset and permissions logic.

    Used by both UI and API views.
    """

    def get_queryset(self):
        """Return a filtered queryset annotated with log count.

        - Staff and superusers see all jobs.
        - Regular users only see their own jobs.
        """
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return qs
        return qs.filter(username=user.username)

    def get_object(self):
        """Return object only if user has permission."""
        obj = super().get_object()
        user = self.request.user
        if user.is_staff or user.is_superuser or obj.username == user.username:
            return obj
        raise PermissionDenied("You do not have permission to access this object.")


class UserViewSet(
    UserQueryMixin,
    viewsets.ModelViewSet,
):
    """REST API endpoints for Job model."""

    serializer_class = UserSerializer
    # filterset_class = UserFilter
    filter_backends = [DjangoFilterBackend]


class UserListView(UserQueryMixin, ObjectListView):
    model = User
    table_class = UserTable
    # filterset_class = ProxmoxHostFilter
    list_view = "user_list"


class UserDetailView(CommonMixin, ObjectDetailView):
    """HTML detail view for a single ProxmoxHost."""

    model = User
    list_view = "user_list"
    # exclude=["id"]
    # sequence=["name", "created_at", "description"]


class UserCreateView(ObjectCreateView):
    model = User
    form_class = UserForm

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
        return reverse("user_detail", kwargs={"pk": self.object.pk})


class UserChangeView(ObjectChangeView):
    model = User
    form_class = UserForm
    # fields = '__all__'
    # template_name = 'object_form.html'
    # success_url = reverse_lazy('home')


# class GroupViewSet(ViewSet):
#     """REST API endpoints for Log model."""

#     serializer_class = LogSerializer
#     filterset_class = LogFilter
#     filter_backends = [DjangoFilterBackend]
#     queryset = Log.objects.all()


class GroupListView(ObjectListView):
    model = Group
    table_class = GroupTable
    filterset_class = GroupFilter
    list_view = "group_list"
    search = True
    # model = Job
    # table_class = JobTable
    # filterset_class = JobFilter


class GroupDetailView(ObjectDetailView):
    """HTML detail view for a single ProxmoxHost."""

    model = Group
    list_view = "group_list"
    # exclude=["id"]
    # sequence=["name", "created_at", "description"]

class GroupCreateView(ObjectCreateView):
    model = Group
    form_class = GroupForm


class GroupChangeView(ObjectChangeView):
    model = Group
    form_class = GroupForm
    # fields = '__all__'
    # template_name = 'object_form.html'
    # success_url = reverse_lazy('home')


class TokenListView(BaseListView):
    model = Token
    table_class = TokenTable
    # filterset_class = ProxmoxHostFilter
    list_view = "token_list"


class TokenDetailView(ObjectDetailView):
    """HTML detail view for a single ProxmoxHost."""

    model = Token
    list_view = "token_detail"
    # exclude=["id"]
    # sequence=["name", "created_at", "description"]
