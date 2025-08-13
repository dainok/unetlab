"""Views, called by URLs."""

from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView
from django.conf import settings
from django.db.models import Count, Prefetch
from rest_framework import viewsets, mixins
from django_filters.views import FilterView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django_tables2 import SingleTableView
from job.models import Log, Job
from job.serializers import JobSerializer, LogSerializer
from job.filters import JobFilter, LogFilter
from job.tables import LogTable, JobTable
from unetlab.utils import db_fields_to_dict
from unetlab.views import CommonMixin, BaseListView
from ui.views import ObjectListView


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
        return qs.filter(username=user.username)

    def get_object(self):
        """Return object only if user has permission."""
        obj = super().get_object()
        user = self.request.user
        if user.is_staff or user.is_superuser or obj.username == user.username:
            return obj
        raise PermissionDenied("You do not have permission to access this object.")


class JobViewSet(
    JobQueryMixin,
    mixins.ListModelMixin,  # GET /job/
    mixins.RetrieveModelMixin,  # GET /job/{id}/
    mixins.DestroyModelMixin,  # DELETE /job/{id}/
    viewsets.GenericViewSet,
):
    """REST API endpoints for Job model."""

    serializer_class = JobSerializer
    filterset_class = JobFilter
    filter_backends = [DjangoFilterBackend]
    queryset = Job.objects.all()


class JobListView(BaseListView):
    """HTML table view for Jobs with filtering and pagination."""

    model = Job
    table_class = JobTable
    filterset_class = JobFilter


class JobDetailView(JobQueryMixin, CommonMixin, DetailView):
    """HTML detail view for a single Job with its logs."""

    model = Job
    template_name = "objects/job_detail.html"

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
        return qs.filter(job__username=user.username)

    def get_object(self):
        """Return object only if user has permission."""
        obj = super().get_object()
        user = self.request.user
        if user.is_staff or user.is_superuser or obj.job.user == user.username:
            return obj
        raise PermissionDenied("You do not have permission to access this object.")


class LogViewSet(
    LogQueryMixin,
    mixins.ListModelMixin,  # GET /log/
    mixins.RetrieveModelMixin,  # GET /log/{id}/
    mixins.DestroyModelMixin,  # DELETE /log/{id}/
    viewsets.GenericViewSet,
):
    """REST API endpoints for Log model."""

    serializer_class = LogSerializer
    filterset_class = LogFilter
    filter_backends = [DjangoFilterBackend]
    queryset = Log.objects.all()

    @action(detail=False, methods=["post"])
    def acknowledge(self, request):
        """Mark all logs as acknowledged for the current user."""
        Log.objects.filter(
            job__username=request.user.username, acknowledged=False
        ).update(acknowledged=True)
        return Response({"status": "ok"}, status=200)


class LogListView(BaseListView):
    """HTML table view for Logs with filtering and pagination."""

    model = Log
    table_class = LogTable
    filterset_class = LogFilter
    vip_actions = ["acknowledge"]


class LogDetailView(LogQueryMixin, CommonMixin, DetailView):
    """HTML detail view for a single Log."""

    model = Log
    template_name = "objects/log_detail.html"

    def get_context_data(self, **kwargs):
        """Add job and log field metadata to context."""
        context = super().get_context_data(**kwargs)
        context["job_fields"] = db_fields_to_dict(Job._meta.fields)
        context["log_fields"] = db_fields_to_dict(Log._meta.fields)
        return context
