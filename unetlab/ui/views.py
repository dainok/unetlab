from typing import Any
from django import forms
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.utils.module_loading import import_string
from django_tables2.columns import Column
from django_tables2 import TemplateColumn
from django.template import Template, Context
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token
from unetlab.views import CommonMixin, BaseListView
from ui.tables import UserTable, GroupTable, TokenTable
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets, permissions
from ui.serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from ui.forms import UserForm, GroupForm, TokenForm
from ui.filters import GroupFilter


class ObjectDetailView(DetailView):
    exclude = []
    sequence = []
    attrs = {"title": "", "description": ""}
    template_name = "objects/object_detail.html"
    list_view = None

    def get_list_view(self):
        if self.list_view is not None:
            return self.list_view
        # Se non definito, calcola da model
        return f"{self.model._meta.model_name}_list"

    def get_column_fields(self):
        """
        Restituisce gli attributi della classe che sono istanze di django_tables2 Column.
        """
        return {
            attr_name: getattr(self.__class__, attr_name)
            for attr_name in dir(self.__class__)
            if isinstance(getattr(self.__class__, attr_name), Column)
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object
        fields = obj._meta.fields

        column_fields = self.get_column_fields()
        data = {}

        for field in fields:
            field_name = field.name
            if field_name in self.exclude:
                continue

            value = getattr(obj, field_name)
            # column = column_fields.get(field_name)

            # if isinstance(column, TemplateColumn):
            #     template = Template(column.template_code)
            #     ctx = Context({"record": obj, "value": value})
            #     value = template.render(ctx)
            # Altri tipi di colonne possono essere gestiti qui se vuoi

            data[field_name] = value

        # Ordina secondo sequence, se presente
        if self.sequence:
            ordered_data = {k: data[k] for k in self.sequence if k in data}
            for k in data:
                if k not in ordered_data:
                    ordered_data[k] = data[k]
            data = ordered_data

        context["object"] = data
        context["attrs"] = {
            "title": self.attrs.get("title", ""),
            "description": self.attrs.get("description", ""),
        }
        context["list_view"] = self.get_list_view()
        return context


class ObjectCreateView(CreateView):
    template_name = "objects/object_form.html"
    # success_url = reverse_lazy('home')


class ObjectChangeView(UpdateView):
    template_name = "objects/object_form.html"
    # success_url = reverse_lazy('home')


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


class UserListView(UserQueryMixin, BaseListView):
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


class GroupListView(BaseListView):
    model = Group
    table_class = GroupTable
    filterset_class = GroupFilter
    list_view = "group_list"
    search = True


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
