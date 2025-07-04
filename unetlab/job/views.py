"""Views, called by URLs."""

from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.db.models import Count, Prefetch
from rest_framework import viewsets, mixins
from django_filters.views import FilterView
from django_filters.rest_framework import DjangoFilterBackend
from job.models import Log, Job
from job.serializers import JobSerializer, LogSerializer
from job.filters import JobFilter, LogFilter
from unetlab.utils import db_fields_to_dict
from unetlab.views import CommonMixin


class JobQueryMixin:
    """Mixin to encapsulate common Job queryset and permissions logic.

    Used by both UI and API views.
    """

    def get_queryset(self):
        """Return a filtered queryset annotated with log count.

        - Staff and superusers see all jobs.
        - Regular users only see their own jobs.
        """
        qs = super().get_queryset()
        qs = qs.annotate(log_count=Count("logs"))
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return qs
        return qs.filter(user=user.username)

    def get_object(self):
        """Return object only if user has permission."""
        obj = super().get_object()
        user = self.request.user
        if user.is_staff or user.is_superuser or obj.user == user.username:
            return obj
        raise PermissionDenied("You do not have permission to access this object.")

    def get_paginate_by(self, queryset):
        """Allow client to customize pagination via 'per_page' query param.

        Enforces a maximum of 100 per page; defaults to 10.
        """
        per_page = self.request.GET.get("per_page")
        try:
            per_page = int(per_page)
            if per_page > 100:
                return 100
            if per_page > 0:
                return per_page
        except (TypeError, ValueError):
            pass
        return 10


class JobViewSet(
    JobQueryMixin,
    mixins.ListModelMixin,  # GET /jobs/
    mixins.RetrieveModelMixin,  # GET /jobs/{id}/
    mixins.DestroyModelMixin,  # DELETE /jobs/{id}/
    viewsets.GenericViewSet,
):
    """REST API endpoints for Job model."""

    serializer_class = JobSerializer
    filterset_class = JobFilter
    filter_backends = [DjangoFilterBackend]
    queryset = Job.objects.all()


class JobListView(JobQueryMixin, CommonMixin, FilterView, ListView):
    """HTML list view for Jobs with filtering and pagination."""

    model = Job
    filterset_class = JobFilter
    paginate_by = settings.REST_FRAMEWORK["PAGE_SIZE"]
    extra_context = {
        "job_fields": db_fields_to_dict(Job._meta.fields),
    }


class JobDetailView(JobQueryMixin, CommonMixin, DetailView):
    """HTML detail view for a single Job with its logs."""

    model = Job

    def get_queryset(self):
        """Prefetch logs ordered by creation date for performance."""
        return Job.objects.prefetch_related(
            Prefetch("logs", queryset=Log.objects.order_by("created_at"))
        )

    def get_context_data(self, **kwargs):
        """Add job and log field metadata and logs list to context."""
        context = super().get_context_data(**kwargs)
        context["job_fields"] = db_fields_to_dict(Job._meta.fields)
        context["log_fields"] = db_fields_to_dict(Log._meta.fields)
        context["log_list"] = self.object.logs.all()
        return context


class LogQueryMixin:
    """Mixin to encapsulate common Log queryset and permissions logic.

    Used by both UI and API views.
    """

    def get_queryset(self):
        """Return a filtered queryset.

        - Staff and superusers see all logs.
        - Regular users see logs only for their jobs.
        """
        qs = super().get_queryset()
        qs = qs.select_related("job")
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return qs
        return qs.filter(job__user=user.username)

    def get_object(self):
        """Return object only if user has permission."""
        obj = super().get_object()
        user = self.request.user
        if user.is_staff or user.is_superuser or obj.job.user == user.username:
            return obj
        raise PermissionDenied("You do not have permission to access this object.")

    def get_paginate_by(self, queryset):
        """Allow client to customize pagination via 'per_page' query param.

        Enforces a maximum of 100 per page; defaults to 10.
        """
        per_page = self.request.GET.get("per_page")
        try:
            per_page = int(per_page)
            if per_page > 100:
                return 100
            if per_page > 0:
                return per_page
        except (TypeError, ValueError):
            pass
        return 10


class LogViewSet(
    LogQueryMixin,
    mixins.ListModelMixin,  # GET /logs/
    mixins.RetrieveModelMixin,  # GET /logs/{id}/
    mixins.DestroyModelMixin,  # DELETE /logs/{id}/
    viewsets.GenericViewSet,
):
    """REST API endpoints for Log model."""

    serializer_class = LogSerializer
    filterset_class = LogFilter
    filter_backends = [DjangoFilterBackend]
    queryset = Log.objects.all()


class LogListView(LogQueryMixin, CommonMixin, FilterView, ListView):
    """HTML list view for Logs with filtering and pagination."""

    model = Log
    filterset_class = LogFilter
    paginate_by = settings.REST_FRAMEWORK["PAGE_SIZE"]
    extra_context = {
        "log_fields": db_fields_to_dict(Log._meta.fields),
        "job_fields": db_fields_to_dict(Job._meta.fields),
    }


class LogDetailView(LogQueryMixin, CommonMixin, DetailView):
    """HTML detail view for a single Log."""

    model = Log

    def get_context_data(self, **kwargs):
        """Add job and log field metadata to context."""
        context = super().get_context_data(**kwargs)
        context["job_fields"] = db_fields_to_dict(Job._meta.fields)
        context["log_fields"] = db_fields_to_dict(Log._meta.fields)
        return context
