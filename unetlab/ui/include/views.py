"""Generic base views and API viewsets for UNetLab.

This module defines reusable CRUD views, detail views, list views, and
API viewsets that can be extended by application-specific models.
It integrates with Django generic views, Django REST Framework,
django-tables2, and django-filters.
"""

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
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


class APICRUDViewSet(ModelViewSet):
    """Base ModelViewSet for full CRUD REST API.

    Subclasses should define `queryset` and `serializer_class`.
    Optional: `filterset_class` for filtering support.
    """

    filterset_class = None
    serializer_class = None
    queryset = None
    permission_classes = [ObjectPermission]  # Required for API


class APIRDViewSet(
    DestroyModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    """Read and delete only REST API viewset.

    Provides list, retrieve, and delete endpoints.
    Subclasses should define `queryset` and `serializer_class`.
    """

    filterset_class = None
    serializer_class = None
    queryset = None
    permission_classes = [ObjectPermission]  # Required for API


class APIRViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Read only REST API viewset.

    Provides list, retrieve, and delete endpoints.
    Subclasses should define `queryset` and `serializer_class`.
    """

    filterset_class = None
    serializer_class = None
    queryset = None
    permission_classes = [ObjectPermission]  # Required for API


class TemplateMixin:
    # Solo per TemplateView
    policy_class = None  # da impostare nelle subclass o nei mixin specifici

    def dispatch(self, request, *args, **kwargs):
        """
        Esegue il controllo dei permessi prima di processare la view.
        """
        policy = self.policy_class()
        result = policy.can(request.user, request.method)
        if result is True:
            return super().dispatch(request, *args, **kwargs)
        elif result is False:
            raise PermissionDenied(
                "Non hai i permessi per eseguire questa azione."
            )  # 403
        elif result is None:
            if settings.LOGIN_URL:
                return HttpResponseRedirect(settings.LOGIN_URL)
            return HttpResponse("Non autenticato", status=401)  # 401
        else:
            # fallback di sicurezza
            return HttpResponse("Errore permessi TemplateView", status=403)


class ObjectMixin:
    """
    Mixin generico per applicare una policy di permessi (es. UserPermissionPolicy)
    a qualsiasi ModelView Django (Create/Update/Delete/List/Detail).

    Solo per CBV.
    """

    policy_class = None  # da impostare nelle subclass o nei mixin specifici

    def dispatch(self, request, *args, **kwargs):
        """
        Esegue il controllo dei permessi prima di processare la view.
        """
        result = self.has_permission()
        if result is True:
            return super().dispatch(request, *args, **kwargs)
        elif result is False:
            raise PermissionDenied(
                "Non hai i permessi per eseguire questa azione."
            )  # 403
        elif result is None:
            if settings.LOGIN_URL:
                return HttpResponseRedirect(settings.LOGIN_URL)
            return HttpResponse("Non autenticato", status=401)  # 401
        else:
            # fallback di sicurezza
            return HttpResponse("Errore permessi ObjectMixin", status=403)

    def has_permission(self):
        """
        Verifica i permessi a livello di view, includendo la normalizzazione del metodo.
        """
        if not self.policy_class:
            return True  # Nessuna policy definita → accesso consentito

        policy = self.policy_class()
        user = self.request.user

        # 🔹 Normalizzazione del metodo (inline)
        method = self.request.method.upper()

        # Normalizza i form POST delle view HTML in "DELETE" o "PUT"
        if method == "POST":
            if isinstance(self, ObjectDeleteView) or isinstance(
                self, ObjectBulkDeleteView
            ):
                method = "DELETE"
            if isinstance(self, ObjectChangeView):
                method = "PUT"
            if isinstance(self, ObjectCreateView):
                method = "POST"

        data = getattr(self.request, "data", None)
        if isinstance(data, list):
            # bulk operation
            for item in data:
                obj = self._resolve_object(item)
                if not policy.can(user, method, obj):
                    raise PermissionDenied(
                        f"Non hai i permessi per modificare l'oggetto {obj}."
                    )
            return True

        # Single object
        target = None
        if hasattr(self, "get_object") and callable(getattr(self, "get_object")):
            try:
                target = self.get_object()
            except Exception:
                target = None

        return policy.can(user, method, target)


class ObjectBulkDeleteView(ObjectMixin, TemplateView):
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

        queryset = self.model.objects.filter(pk__in=ids)
        if not queryset:
            # Objects do not exist, there is nothing to delete
            return redirect(self.get_success_url())

        if "confirm" in request.POST:
            # Last step: the form has passed confirm, we proceed with the cancellation
            queryset.delete()
            return redirect(self.get_success_url())

        # Penultimate step: the user must confirm the list of objects to be deleted
        context = self.get_context_data()
        context["object_list"] = queryset
        return render(
            request,
            self.template_name,
            context,
        )


class ObjectChangeView(ObjectMixin, UpdateView):
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

    def get_form_kwargs(self):
        # recupera i kwargs standard
        kwargs = super().get_form_kwargs()
        # aggiunge l'utente corrente
        kwargs["user"] = self.request.user
        return kwargs


class ObjectCreateView(ObjectMixin, CreateView):
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

    def get_form_kwargs(self):
        # recupera i kwargs standard
        kwargs = super().get_form_kwargs()
        # aggiunge l'utente corrente
        kwargs["user"] = self.request.user
        return kwargs


class ObjectDeleteView(ObjectMixin, DeleteView):
    """Generic delete view with confirmation for a single object.

    Subclasses should define `model`.
    Uses `ui/object_confirm_delete.html` template.
    """

    model = None
    form_class = None
    template_name = "ui/object_confirm_delete.html"

    def get_success_url(self):
        """Redirect to the list page of the model after deletion."""
        model_name = self.model._meta.model_name
        return reverse_lazy(f"{model_name}_list")

    def post(self, request, *args, **kwargs):
        """
        Forza la chiamata diretta a delete(), ignorando eventuali mixin
        che ereditano da FormMixin e provano a usare un form.
        """
        self.object = self.get_object()
        return self.delete(request, *args, **kwargs)


class ObjectDetailView(ObjectMixin, DetailView):
    """Generic detail view for any model object.

    Provides field data as a dictionary, supports column ordering,
    and custom attributes for title and description in context.
    """

    model = None
    exclude = []
    sequence = []
    attrs = {}
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
        # fields = obj._meta.fields
        policy = self.policy_class()
        user = self.request.user

        class SingleObjectTable(tables.Table):
            class Meta:
                model = self.model
                template_name = "django_tables2/bootstrap.html"
                # Se vuoi, puoi escludere campi dinamicamente
                exclude = self.exclude
                sequence = self.sequence
                attrs = self.attrs

        for custom_field in self.get_column_fields().keys():
            # custom_fields[custom_field] = getattr(self, custom_field)
            SingleObjectTable.base_columns[custom_field] = getattr(self, custom_field)
        table = SingleObjectTable([obj])
        RequestConfig(self.request).configure(table)
        # context["table"] = list(table.rows)[0]

        # for field_name in self.exclude:
        #     # Removing excluded fields
        #     if field_name in data:
        #         del data[field_name]

        # # Sort by `sequence`, if present
        # if self.sequence:
        #     ordered_data = {k: data[k] for k in self.sequence if k in data}
        #     for k in data:
        #         if k not in ordered_data:
        #             ordered_data[k] = data[k]
        #     data = ordered_data

        context["object"] = list(table.rows)[0]
        context["attrs"] = {
            "title": self.attrs.get("title", str(obj)),
            "description": self.attrs.get("description", ""),
            "name": str(obj),
            # "fields": {},
        }
        # for field_name, value in data.items():
        #     try:
        #         field = obj._meta.get_field(field_name)
        #         context["attrs"]["fields"][field.name] = {
        #             "verbose_name": field.verbose_name,
        #             "help_text": field.help_text,
        #         }
        #     except FieldDoesNotExist:
        #         field = None

        #     custom_field = getattr(self, field_name, None)
        #     if custom_field:
        #         if custom_field.verbose_name:
        #             context["attrs"]["fields"][field.name]["verbose_name"] = custom_field.verbose_name
        #         if custom_field.template_name:
        #             context["attrs"]["fields"][field.name]["template_name"] = custom_field.template_name

        # else:
        # print(help(obj._meta.get_field))

        # for field in obj._meta.get_fields():
        #     if field.concrete and not field.many_to_many and not field.auto_created:
        #         context["attrs"]["fields"][field.name] = {
        #             "verbose_name": field.verbose_name,
        #             "help_text": field.help_text,
        #         }
        #         custom_field = getattr(self, field.name, None)
        #         if custom_field:
        #             context["attrs"]["fields"][field.name]["template_name"] = custom_field.template_name
        #             if custom_field.verbose_name:
        #                 # Override verbose name
        #                 context["attrs"]["fields"][field.name]["verbose_name"] = custom_field.verbose_name
        context["model_name"] = self.model._meta.model_name
        context["permissions"] = {
            "can_create": policy.can(user, "POST"),
            "can_read": True,
            "can_update": policy.can(user, "PATCH", obj),
            "can_delete": policy.can(user, "DELETE", obj),
        }
        context["pk"] = obj.pk
        return context


class ObjectListView(ObjectMixin, SingleTableView, FilterView):
    """Base list view using django-tables2 and django-filters.

    Supports pagination customization via 'per_page' query param.
    Subclasses should define `model`, `table_class`, and optionally `filterset_class`.
    """

    filterset_class = None
    model = None
    table_class = None

    paginate_by = settings.DJANGO_TABLES2_PAGE_SIZE
    template_name = "ui/object_list.html"

    # def render_to_response(self, context, **response_kwargs):
    #     queryset = context['object_list']

    #     # Paginazione
    #     page = int(self.request.GET.get("page", 1))
    #     per_page = int(self.request.GET.get("per_page", 10))
    #     paginator = Paginator(queryset, per_page)
    #     page_obj = paginator.get_page(page)

    #     # Serializzazione
    #     serializer = UserSerializer(page_obj, many=True)
    #     data = {
    #         "results": serializer.data,
    #         "count": paginator.count,
    #         "num_pages": paginator.num_pages,
    #     }

    #     # Ritorna JSON se richiesto
    #     # if self.request.headers.get("Accept") == "application/json":
    #     #     return JsonResponse(data, safe=False)

    #     # Altrimenti fallback al template HTML
    #     return super().render_to_response(context, **response_kwargs)

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
        context["model_name"] = self.model._meta.model_name
        context["permissions"] = {
            "can_create": policy.can(user, "POST"),
            "can_read": True,
            "can_update": True,
            "can_delete": True,
        }
        # Add filters
        filterset = self.get_filterset(self.get_filterset_class())
        if filterset:
            context["filter"] = filterset
        return context
