"""Generic base views and API viewsets for UNetLab.

This module defines reusable CRUD views, detail views, list views, and
API viewsets that can be extended by application-specific models.
It integrates with Django generic views, Django REST Framework,
django-tables2, and django-filters.
"""

from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django_filters.views import FilterView
from django_tables2 import SingleTableView
from django_tables2.columns import Column
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet
from unetlab.views import CommonMixin


class APICRUDViewSet(ModelViewSet):
    """Base ModelViewSet for full CRUD REST API.

    Subclasses should define `queryset` and `serializer_class`.
    Optional: `filterset_class` for filtering support.
    """

    filterset_class = None
    serializer_class = None
    queryset = None


class APIRDViewSet(DestroyModelMixin, ListModelMixin, RetrieveModelMixin):
    """Read and delete only REST API viewset.

    Provides list, retrieve, and delete endpoints.
    Subclasses should define `queryset` and `serializer_class`.
    """

    filterset_class = None
    serializer_class = None
    queryset = None


class ObjectChangeView(CommonMixin, UpdateView):
    """Generic update view for any model object.

    Subclasses should define `model` and `form_class`.
    Uses `ui/object_form.html` template.
    """

    model = None
    template_name = "ui/object_form.html"
    form_class = None

    def get_success_url(self):
        """Redirect to the object's detail page after successful update."""
        model_name = self.model._meta.model_name
        return reverse(f"{model_name}_detail", kwargs={"pk": self.object.pk})


class ObjectCreateView(CommonMixin, CreateView):
    """Generic create view for any model object.

    Subclasses should define `model` and optionally `form_class`.
    Uses `ui/object_form.html` template.
    """

    model = None
    template_name = "ui/object_form.html"

    def get_success_url(self):
        """Redirect to the list page of the model after creation."""
        model_name = self.model._meta.model_name
        return reverse(f"{model_name}_list")


class ObjectDeleteView(CommonMixin, DeleteView):
    """Generic delete view with confirmation for a single object.

    Subclasses should define `model`.
    Uses `ui/object_confirm_delete.html` template.
    """

    model = None
    template_name = "ui/object_confirm_delete.html"

    def get_success_url(self):
        """Redirect to the list page of the model after deletion."""
        model_name = self.model._meta.model_name
        return reverse_lazy(f"{model_name}_list")


class ObjectBulkDeleteView(CommonMixin, View):
    """Generic view to delete multiple objects selected via checkboxes.

    Subclasses should define `model`.
    """

    model = None
    template_name = "ui/object_confirm_delete.html"

    def get_success_url(self):
        """Redirect to the model's list view after deletion."""
        model_name = self.model._meta.model_name
        return reverse_lazy(f"{model_name}_list")

    def post(self, request, *args, **kwargs):
        """Handle bulk deletion from POST data.

        Expects 'selected_ids' list from POST. If 'confirm' is present,
        deletes the objects; otherwise renders a confirmation template.
        """
        # The list of IDs is passed as list selected_ids from the form
        ids = request.POST.getlist("selected_ids")
        if not ids:
            # The list is empty, there is nothing to delete
            return redirect(self.get_success_url())

        queryset = self.model.objects.filter(id__in=ids)
        if not queryset:
            # Objects do not exist, there is nothing to delete
            return redirect(self.get_success_url())

        if "confirm" in request.POST:
            # Last step: the form has passed confirm, we proceed with the cancellation
            queryset.delete()
            return redirect(self.get_success_url())

        # Penultimate step: the user must confirm the list of objects to be deleted
        return render(
            request,
            self.template_name,
            {
                "object_list": queryset,
            },
        )


class ObjectDetailView(CommonMixin, DetailView):
    """Generic detail view for any model object.

    Provides field data as a dictionary, supports column ordering,
    and custom attributes for title and description in context.
    """

    model = None
    exclude = []
    sequence = []
    attrs = {"title": "", "description": ""}
    template_name = "ui/object_detail.html"
    list_view = None

    def get_column_fields(self):
        """Return all class attributes that are django_tables2 Column instances."""
        return {
            attr_name: getattr(self.__class__, attr_name)
            for attr_name in dir(self.__class__)
            if isinstance(getattr(self.__class__, attr_name), Column)
        }

    def get_context_data(self, **kwargs):
        """Prepare context data for template rendering."""
        context = super().get_context_data(**kwargs)
        obj = self.object
        fields = obj._meta.fields

        data = {}

        for field in fields:
            field_name = field.name
            if field_name in self.exclude:
                continue
            value = getattr(obj, field_name)
            data[field_name] = value

        # Sort by `sequence`, if present
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
        context["model_name"] = self.model._meta.model_name
        context["pk"] = obj.pk
        return context


class ObjectListView(CommonMixin, SingleTableView, FilterView):
    """Base list view using django-tables2 and django-filters.

    Supports pagination customization via 'per_page' query param.
    Subclasses should define `model`, `table_class`, and optionally `filterset_class`.
    """

    filterset_class = None
    model = None
    table_class = None

    paginate_by = settings.DJANGO_TABLES2_PAGE_SIZE
    template_name = "ui/object_list.html"

    def get_table(self, **kwargs):
        """Return the table instance. Placeholder for custom pagination logic."""
        # PAGINATE NOT WORKING TODO
        table = super().get_table(**kwargs)
        print("paginate_by in view:", self.get_paginate_by(table.data))
        return table

    def get_table_data(self):
        """Return the queryset filtered by the FilterSet if present."""
        queryset = super().get_table_data()
        filterset_class = self.get_filterset_class()
        if filterset_class:
            filterset = filterset_class(self.request.GET, queryset=queryset)
            return filterset.qs
        return queryset

    def get_paginate_by(self, queryset):
        """Allow client to customize pagination via 'per_page' query param.

        Enforces a maximum of DJANGO_TABLES2_MAX_PAGE_SIZE per page; defaults to
        DJANGO_TABLES2_PAGE_SIZE if invalid or missing.
        """
        # PAGINATE NOT WORKING TODO
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

    def get_context_data(self, **kwargs):
        """Add model name to context for template rendering."""
        context = super().get_context_data(**kwargs)
        # Add model_name to create URLs via views
        context["model_name"] = self.model._meta.model_name
        # Add filters
        filterset = self.get_filterset(self.get_filterset_class())
        if filterset:
            context["filter"] = filterset
        return context
