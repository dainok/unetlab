"""Generic base views and API viewsets."""

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django_filters.views import FilterView
from django_tables2 import SingleTableView
from django_tables2.columns import Column
from django_tables2 import RequestConfig
import django_tables2 as tables
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from ui.include.permissions import ObjectPermission


#############################################################################
# DRF (API)
#############################################################################


class APICRUDViewSet(ModelViewSet):
    """Base ModelViewSet for full CRUD REST API."""

    filterset_class = None
    permission_classes = [ObjectPermission]  # Required for API
    queryset = None
    serializer_class = None


class APIRDViewSet(
    DestroyModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    """Read and delete only REST API viewset."""

    filterset_class = None
    permission_classes = [ObjectPermission]  # Required for API
    queryset = None
    serializer_class = None


class APIRViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Read only REST API viewset."""

    filterset_class = None
    permission_classes = [ObjectPermission]  # Required for API
    queryset = None
    serializer_class = None


#############################################################################
# Models
#############################################################################


class ObjectMixin:
    """Mixin encapsulating permission logic for generic objects."""

    policy_class = None

    def dispatch(self, request, *args, **kwargs):
        """Check permissions before processing the view."""
        result = self.has_permission()
        if result is True:
            # Access granted
            return super().dispatch(request, *args, **kwargs)
        elif result is False:
            # Access denied
            raise PermissionDenied()  # 403
        elif result is None:
            # Guest access is denied
            if settings.LOGIN_URL:
                # If LOGIN_URL is set, redirect to login page
                return HttpResponseRedirect(settings.LOGIN_URL)
            return HttpResponse(status=401)  # 401

        # Fallback
        return HttpResponse(_('Generic permission error'), status=500)

    def has_permission(self):
        """Verify view level permissions using normalized HTTP methods (HTML only)."""
        if not self.policy_class:
            # Access granted without policy_class
            return True

        policy = self.policy_class()
        user = self.request.user
        payload = self.request.POST.dict()

        # HTTP method normalization
        method = self.request.method.upper()
        if method == 'POST':
            # POST is used to delete andmodify
            if isinstance(self, ObjectDeleteView) or isinstance(
                self, ObjectBulkDeleteView
            ):
                # ObjectDeleteView -> translate to DELETE
                method = 'DELETE'
            if isinstance(self, ObjectChangeView):
                # ObjectChangeView -> translate to PUT
                method = 'PUT'
                # ObjectCreateView -> translate to POST
            if isinstance(self, ObjectCreateView):
                method = 'POST'

        data = getattr(self.request, 'data', None)
        if isinstance(data, list):
            # Bulk operation
            for item in data:
                obj = self._resolve_object(item)
                if not policy.can(user, method, obj):
                    raise PermissionDenied(
                        _('You do not have permission to edit %(obj)s')
                        % {'obj': str(obj)}
                    )
            return True

        # Single object
        target = None
        if hasattr(self, 'get_object') and callable(getattr(self, 'get_object')):
            try:
                target = self.get_object()
            except Exception:
                target = None

        return policy.can(user, method, target, payload)

    def get_context_data(self, **kwargs):
        """Add UI settings to all HTML views."""
        context = super().get_context_data(**kwargs)
        context['site_meta'] = settings.SITE_META
        context['site_navbar'] = settings.SITE_NAVBAR
        return context


class ObjectBulkDeleteView(ObjectMixin, TemplateView):
    """Generic view to delete multiple objects selected via checkboxes."""

    model = None
    template_name = 'ui/object_confirm_delete.html'

    def get_success_url(self):
        """Redirect to the model's list view after deletion."""
        model_name = self.model._meta.model_name
        return reverse_lazy(f'{model_name}_list')

    def post(self, request, *args, **kwargs):
        """Handle bulk deletion from POST data.

        Expects selected_ids list from POST. If confirm is present,
        deletes the objects; otherwise renders a confirmation template.
        """
        # The list of IDs is passed as list selected_ids from the form
        ids = request.POST.getlist('selected_ids')
        if not ids:
            # The list is empty, there is nothing to delete
            return redirect(self.get_success_url())

        queryset = self.model.objects.filter(pk__in=ids)
        if not queryset:
            # Objects do not exist, there is nothing to delete
            return redirect(self.get_success_url())

        if 'confirm' in request.POST:
            # Last step: the form has passed confirm, we proceed with the cancellation
            queryset.delete()
            return redirect(self.get_success_url())

        # Penultimate step: the user must confirm the list of objects to be deleted
        context = self.get_context_data()
        context['object_list'] = queryset
        return render(
            request,
            self.template_name,
            context,
        )


class ObjectChangeView(ObjectMixin, UpdateView):
    """Generic update view for any model object."""

    form_class = None
    model = None
    template_name = 'ui/object_form.html'

    def get_success_url(self):
        """Redirect to the object's detail page after successful update."""
        model_name = self.model._meta.model_name
        return reverse(f'{model_name}_detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Add current user
        kwargs['user'] = self.request.user
        return kwargs


class ObjectCreateView(ObjectMixin, CreateView):
    """Generic create view for any model object."""

    model = None
    template_name = 'ui/object_form.html'

    def get_success_url(self):
        """Redirect to the list page of the model after creation."""
        model_name = self.model._meta.model_name
        return reverse(f'{model_name}_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Add current user
        kwargs['user'] = self.request.user
        return kwargs


class ObjectDeleteView(ObjectMixin, DeleteView):
    """Generic delete view with confirmation for a single object."""

    form_class = None
    model = None
    template_name = 'ui/object_confirm_delete.html'

    def get_success_url(self):
        """Redirect to the list page of the model after deletion."""
        model_name = self.model._meta.model_name
        return reverse_lazy(f'{model_name}_list')

    def post(self, request, *args, **kwargs):
        """Ignore mixins and call delete()."""
        self.object = self.get_object()
        return self.delete(request, *args, **kwargs)


class ObjectDetailView(ObjectMixin, DetailView):
    """
    Generic detail view for any model object.

    Use django-tables2 with a single row.
    """

    attrs = {}
    exclude = []
    list_view = None
    model = None
    sequence = []
    template_name = 'ui/object_detail.html'

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
        policy = self.policy_class()
        user = self.request.user

        class SingleObjectTable(tables.Table):
            """Single row Table."""

            class Meta:
                """Meta options."""

                model = self.model
                template_name = 'django_tables2/bootstrap.html'
                exclude = self.exclude
                sequence = self.sequence
                attrs = self.attrs

        for custom_field in self.get_column_fields().keys():
            # Read custom attribute format
            SingleObjectTable.base_columns[custom_field] = getattr(self, custom_field)

        # Create the single row table
        table = SingleObjectTable([obj])
        RequestConfig(self.request).configure(table)

        # Pass data to the template
        context['object'] = list(table.rows)[0]
        context['attrs'] = {
            'title': self.attrs.get('title', str(obj)),
            'description': self.attrs.get('description', ''),
            'name': str(obj),
        }
        context['model_name'] = self.model._meta.model_name
        context['permissions'] = {
            'can_create': policy.can(user, 'POST', None, None),
            'can_read': True,
            'can_update': policy.can(user, 'PATCH', obj, None),
            'can_delete': policy.can(user, 'DELETE', obj, None),
        }
        context['pk'] = obj.pk
        return context


class ObjectListView(ObjectMixin, SingleTableView, FilterView):
    """Generic list view using django-tables2 and django-filters."""

    filterset_class = None
    model = None
    paginate_by = settings.DJANGO_TABLES2_PAGE_SIZE
    table_class = None
    template_name = 'ui/object_list.html'

    def get_table_data(self):
        """Return the queryset filtered by the FilterSet if present."""
        queryset = super().get_table_data()
        filterset_class = self.get_filterset_class()
        if filterset_class:
            filterset = filterset_class(self.request.GET, queryset=queryset)
            return filterset.qs
        return queryset

    def get_context_data(self, **kwargs):
        """Add model name to context for template rendering."""
        policy = self.policy_class()
        user = self.request.user
        context = super().get_context_data(**kwargs)
        # Add model_name to create URLs via views
        context['model_name'] = self.model._meta.model_name
        context['permissions'] = {
            'can_create': policy.can(user, 'POST', None, None),
            'can_read': True,
            'can_update': True,
            'can_delete': True,
        }
        # Add filters
        filterset = self.get_filterset(self.get_filterset_class())
        if filterset:
            context['filter'] = filterset
        return context


#############################################################################
# Template
#############################################################################


class TemplateMixin:
    policy_class = None

    def dispatch(self, request, *args, **kwargs):
        """Check permissions before processing the view."""
        policy = self.policy_class()
        result = policy.can(request.user, request.method, None, None)
        if result is True:
            # Access granted
            return super().dispatch(request, *args, **kwargs)
        elif result is False:
            # Access denied
            raise PermissionDenied()  # 403
        elif result is None:
            # Guest access is denied
            if settings.LOGIN_URL:
                # If LOGIN_URL is set, redirect to login page
                return HttpResponseRedirect(settings.LOGIN_URL)
            return HttpResponse(status=401)  # 401

        # Fallback
        return HttpResponse(_('Generic permission error'), status=500)

    def get_context_data(self, **kwargs):
        """Add UI settings to all HTML views."""
        context = super().get_context_data(**kwargs)
        context['site_meta'] = settings.SITE_META
        context['site_navbar'] = settings.SITE_NAVBAR
        return context
