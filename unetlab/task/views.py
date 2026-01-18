"""Views for Task app."""

from django.db.models import Count, Prefetch
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from django_tables2 import RequestConfig
from task.models import Log, Task
from task.serializers import TaskSerializer, LogSerializer
from task.filters import TaskFilter, LogFilter
from task.tables import LogTable, TaskTable, TaskDetailLogTable
from ui.include.views import (
    APIRDViewSet,
    APIRViewSet,
    ObjectBulkDeleteView,
    ObjectDeleteView,
    ObjectDetailView,
    ObjectListView,
)


#############################################################################
# Task
#############################################################################


class TaskQueryMixin:
    """Mixin encapsulating common queryset and permission logic for Task objects."""

    def get_queryset(self):
        """Return the queryset of Lab objects accessible to the current user."""
        qs = super().get_queryset()
        qs = qs.annotate(log_count=Count('logs'))
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return qs
        return qs.filter(username=user.username)


class TaskAPIViewSet(TaskQueryMixin, APIRDViewSet):
    """REST API ViewSet for the Task model."""


class TaskBulkDeleteView(TaskQueryMixin, ObjectBulkDeleteView):
    """HTML view for deleting multiple Task objects at once."""


class TaskDeleteView(TaskQueryMixin, ObjectDeleteView):
    """HTML view for deleting a single Task."""


class TaskDetailView(TaskQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a Task."""

    template_name = 'task_detail.html'

    def get_queryset(self):
        """Prefetch logs ordered by creation date for performance."""
        return Task.objects.prefetch_related(Prefetch('logs', queryset=Log.objects.order_by('created_at')))

    def get_context_data(self, **kwargs):
        """Add Task and log field metadata and logs list to context."""
        context = super().get_context_data(**kwargs)

        # Log table
        Task_obj = self.object
        log_qs = Task_obj.logs.all()
        log_table = TaskDetailLogTable(log_qs)
        RequestConfig(self.request, paginate=False).configure(log_table)
        context['log_table'] = log_table

        return context


class TaskListView(TaskQueryMixin, ObjectListView):
    """HTML view for displaying a table of Task objects."""


#############################################################################
# Log
#############################################################################


class LogQueryMixin:
    """Mixin encapsulating common queryset and permission logic for Log objects."""

    def get_queryset(self):
        """Return the queryset of Log objects accessible to the current user."""
        qs = super().get_queryset()
        qs = qs.select_related('Task')
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return qs
        return qs.filter(Task__username=user.username)


class LogAPIViewSet(LogQueryMixin, APIRViewSet):
    """REST API ViewSet for the Task model."""

    @action(detail=False, methods=['post'])
    def acknowledge(self, request):
        """Mark all Log objects as acknowledged for the current user."""
        Log.objects.filter(Task__username=request.user.username, acknowledged=False).update(acknowledged=True)
        return Response({'status': 'ok'}, status=200)


class LogDetailView(LogQueryMixin, ObjectDetailView):
    """HTML view for displaying the details of a Log."""

    model = Log
    template_name = 'log_detail.html'


class LogListView(LogQueryMixin, ObjectListView):
    """HTML view for displaying a table of Log objects."""

    filterset_class = LogFilter
    model = Log
    table_class = LogTable
    table_vip_actions = [
        {
            'button': 'acknowledge',
            'js': 'LogAcknowledgeView()',
        }
    ]
