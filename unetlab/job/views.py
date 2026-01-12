"""Views, called by URLs."""

from django.db.models import Count, Prefetch
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from django_tables2 import RequestConfig
from job.models import Log, Job
from job.serializers import JobSerializer, LogSerializer
from job.filters import JobFilter, LogFilter
from job.tables import LogTable, JobTable, JobDetailLogTable
from ui.include.views import (
    APIRDViewSet,
    APIRViewSet,
    ObjectBulkDeleteView,
    ObjectDeleteView,
    ObjectDetailView,
    ObjectListView,
)


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
        qs = qs.annotate(log_count=Count('logs'))
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
        raise PermissionDenied('You do not have permission to access this object.')


class JobAPIViewSet(JobQueryMixin, APIRDViewSet):
    """REST API endpoints for Job model."""

    serializer_class = JobSerializer
    filterset_class = JobFilter


class JobBulkDeleteView(JobQueryMixin, ObjectBulkDeleteView):
    """HTML view for deleting multiple `User` objects at once."""

    model = Job


class JobDeleteView(JobQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single `User`."""

    model = Job


class JobDetailView(JobQueryMixin, ObjectDetailView):
    """HTML detail view for a single Job with its logs."""

    model = Job
    template_name = 'job_detail.html'

    def get_queryset(self):
        """Prefetch logs ordered by creation date for performance."""
        return Job.objects.prefetch_related(
            Prefetch('logs', queryset=Log.objects.order_by('created_at'))
        )

    def get_context_data(self, **kwargs):
        """Add job and log field metadata and logs list to context."""
        context = super().get_context_data(**kwargs)

        # Log table
        job_obj = self.object
        log_qs = job_obj.logs.all()
        log_table = JobDetailLogTable(log_qs)
        RequestConfig(self.request, paginate=False).configure(log_table)
        context['log_table'] = log_table

        return context


class JobListView(JobQueryMixin, ObjectListView):
    """HTML table view for Jobs with filtering and pagination."""

    filterset_class = JobFilter
    model = Job
    table_class = JobTable


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
        qs = qs.select_related('job')
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
        raise PermissionDenied('You do not have permission to access this object.')


class LogAPIViewSet(LogQueryMixin, APIRViewSet):
    """REST API endpoints for Log model."""

    serializer_class = LogSerializer
    filterset_class = LogFilter

    @action(detail=False, methods=['post'])
    def acknowledge(self, request):
        """Mark all logs as acknowledged for the current user."""
        Log.objects.filter(
            job__username=request.user.username, acknowledged=False
        ).update(acknowledged=True)
        return Response({'status': 'ok'}, status=200)


class LogDetailView(LogQueryMixin, ObjectDetailView):
    """HTML detail view for a single Log."""

    model = Log
    template_name = 'log_detail.html'


class LogListView(LogQueryMixin, ObjectListView):
    """HTML table view for Logs with filtering and pagination."""

    filterset_class = LogFilter
    model = Log
    table_class = LogTable
    table_vip_actions = [
        {
            'button': 'acknowledge',
            'js': 'LogAcknowledgeView()',
        }
    ]
