from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, permissions
from django_filters.views import FilterView
from django_filters.rest_framework import DjangoFilterBackend
from django_tables2 import SingleTableView
from django_tables2.columns import Column
from ui.filters import GroupFilter
from ui.forms import GroupForm, TokenForm, UserForm
from ui.serializers import UserSerializer
from unetlab.views import CommonMixin, BaseListView, LogListMixin


class ObjectChangeView(UpdateView):
    template_name = "ui/object_form.html"
    def get_success_url(self):
        model_name = self.model._meta.model_name
        return reverse(f"{model_name}_detail", kwargs={"pk": self.object.pk})

class ObjectCreateView(CreateView):
    template_name = "ui/object_form.html"
    def get_success_url(self):
        model_name = self.model._meta.model_name
        return reverse(f"{model_name}_detail", kwargs={"pk": self.object.pk})

class ObjectDetailView(DetailView):
    exclude = []
    sequence = []
    attrs = {"title": "", "description": ""}
    template_name = "ui/object_detail.html"
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



class ObjectListView(LogListMixin, SingleTableView, FilterView):
    """Base list view with tables2 and django-filters."""

    paginate_by = settings.DJANGO_TABLES2_PAGE_SIZE
    template_name = "ui/object_list.html"

    def get_table(self, **kwargs):
        # PAGINATE NOT WORKING TODO
        table = super().get_table(**kwargs)
        print("paginate_by in view:", self.get_paginate_by(table.data))
        return table

    def get_paginate_by(self, queryset):
        # PAGINATE NOT WORKING TODO
        """Allow client to customize pagination via 'per_page' query param.

        Enforces a maximum of DJANGO_TABLES2_MAX_PAGE_SIZE per page; defaults to DJANGO_TABLES2_PAGE_SIZE.
        """
        try:
            per_page = int(self.request.GET.get("per_page", 0))
            print(per_page)
            if per_page <= 0:
                return settings.DJANGO_TABLES2_PAGE_SIZE
            print("FIX")
            print(min(per_page, settings.DJANGO_TABLES2_MAX_PAGE_SIZE))
            return min(per_page, settings.DJANGO_TABLES2_MAX_PAGE_SIZE)
        except (TypeError, ValueError):
            # return super().get_paginate_by(queryset)
            return settings.DJANGO_TABLES2_PAGE_SIZE
        # table = super().get_table(**kwargs)
        # try:
        #     per_page = int(self.request.GET.get("per_page", 0))
        #     if per_page <= 0:
        #         per_page = settings.DJANGO_TABLES2_PAGE_SIZE
        #     else:
        #         per_page = min(per_page, settings.DJANGO_TABLES2_MAX_PAGE_SIZE)
        #         per_page = 5 # REMOVE TODO
        # except (TypeError, ValueError):
        #     per_page = settings.DJANGO_TABLES2_PAGE_SIZE
        # print(per_page)
        # RequestConfig(self.request, paginate={"per_page": per_page}).configure(table)
        # return table

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     filterset = self.get_filterset(self.get_filterset_class())
    #     context["filter"] = filterset
    #     context["actions"] = self.get_actions()
    #     context["vip_actions"] = self.get_vip_actions()
    #     return context

