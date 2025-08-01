"""Views for UNetLab: entry points bound to URLs."""

from django.views.generic import TemplateView
from django.conf import settings
from django_tables2 import SingleTableView
from django_filters.views import FilterView
from django_tables2 import RequestConfig
from job.models import Log
from job.tables import LogHomeTable
from proxmox.tables import ProxmoxHostHomeTable
from proxmox.models import ProxmoxHost


class CommonMixin:
    """HTML list view with filtering and pagination."""

    def get_log_queryset(self):
        """Return un-ancknoledged logs, owned by the user."""
        user = self.request.user
        qs = Log.objects.filter(
            acknowledged=False, job__username=user.username
        ).order_by("-created_at")[:10]
        return qs

    def get_context_data(self, **kwargs):
        """Add latest logs to context."""
        context = super().get_context_data(**kwargs)
        context["latest_logs"] = self.get_log_queryset()
        return context


class CommonListMixin:
    """HTML list view with filtering and pagination."""

    actions = []  # General actions (e.g., 'delete', 'add')
    vip_actions = []  # VIP actions (e.g., 'host-rescan')

    def get_paginate_by(self, queryset):
        """Allow client to customize pagination via 'per_page' query param.

        Enforces a maximum of 100 per page; defaults to 10.
        """
        # TODO: not working
        per_page = self.request.GET.get("per_page")
        try:
            per_page = int(per_page)
            if per_page > 100:
                return 100
            if per_page > 0:
                return per_page
        except (TypeError, ValueError):
            pass
        return settings.REST_FRAMEWORK["PAGE_SIZE"]

    def get_context_data(self, **kwargs):
        """Add latest logs to context."""
        # TODO: not working
        context = super().get_context_data(**kwargs)
        context["actions"] = self.get_actions()
        context["vip_actions"] = self.get_vip_actions()
        return context

    def get_actions(self):
        """Return standard actions, can be overridden."""
        return self.actions

    def get_vip_actions(self):
        """Return VIP actions, can be overridden."""
        return self.vip_actions


class BaseListView(CommonMixin, CommonListMixin, SingleTableView, FilterView):
    """Base list view with tables2 and django-filters."""

    paginate_by = settings.REST_FRAMEWORK["PAGE_SIZE"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filterset = self.get_filterset(self.get_filterset_class())
        context["filter"] = filterset
        context["actions"] = self.get_actions()
        context["vip_actions"] = self.get_vip_actions()
        return context


class HomeView(CommonMixin, TemplateView):
    """
    Render the home page for authenticated users.

    The template is loaded from: templates/unetlab/home.html
    """

    template_name = "unetlab/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Log table
        log_qs = Log.objects.filter(
            severity__gte=30, job__username=user.username
        ).order_by("-created_at")
        log_qs = list(log_qs[:10])
        log_table = LogHomeTable(log_qs)
        RequestConfig(self.request, paginate=False).configure(log_table)
        context["log_table"] = log_table

        # Host table
        host_qs = ProxmoxHost.objects.all()
        host_table = ProxmoxHostHomeTable(host_qs)
        RequestConfig(self.request, paginate=False).configure(host_table)
        context["host_table"] = host_table

        return context
