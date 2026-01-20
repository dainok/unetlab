"""Table definitions for Task app."""

from django.utils.translation import gettext_lazy as _
import django_tables2 as tables
from task.models import Log, Task
from ui.include.tables import (
    GreenBooleanColumn,
    ObjectTable,
    SeverityAllColumn,
)


#############################################################################
# Task
#############################################################################


class TaskTable(tables.Table):
    id = tables.LinkColumn(
        'task_detail',
        args=[tables.A('pk')],
    )
    log_count = tables.Column(orderable=False, verbose_name=_('Logs'), attrs={'td': {'class': 'text-center'}})
    created_at = tables.DateColumn(orderable=True, format='Y-m-d H:i')
    updated_at = tables.DateColumn(orderable=True, format='Y-m-d H:i')

    class Meta:
        model = Task
        sequence = ['id', 'name', 'user', 'status', 'log_count', 'created_at', 'updated_at']
        fields = [f.name for f in Task._meta.fields] + ['log_count']
        exclude = ['select', 'updated_at']
        order_by = '-updated_at'
        attrs = {
            'title': "DACAMBIARE",
            'description': "DACAMBIARE",
            'search': True,
            'table_actions': [],
            'row_actions': [],
        }


class TaskDetailLogTable(ObjectTable):
    id = tables.LinkColumn(
        'log_detail',
        args=[tables.A('pk')],
    )
    acknowledged = GreenBooleanColumn(orderable=True, verbose_name=_('Ack'), attrs={'td': {'class': 'text-center'}})
    severity = SeverityAllColumn(orderable=True, verbose_name=_('Sev'), attrs={'td': {'class': 'text-center'}})
    created_at = tables.DateColumn(orderable=True, format='Y-m-d H:i')

    class Meta:
        model = Log
        sequence = ['id', 'severity', 'type', '...']
        exclude = ['select', 'source', 'task', 'updated_at']
        attrs = {
            'title': 'Related Logs',
            'table_actions': [],
            'row_actions': [],
        }


#############################################################################
# Log
#############################################################################


class LogTable(ObjectTable):
    id = tables.LinkColumn(
        'log_detail',
        args=[tables.A('pk')],
    )
    acknowledged = GreenBooleanColumn(orderable=True, verbose_name=_('Ack'), attrs={'td': {'class': 'text-center'}})
    severity = SeverityAllColumn(orderable=True, verbose_name=_('Sev'), attrs={'td': {'class': 'text-center'}})
    created_at = tables.DateColumn(orderable=True, format='Y-m-d H:i')

    class Meta:
        model = Log
        sequence = ['id', 'severity', 'acknowledged', 'type', '...']
        exclude = ['select', 'source', 'task', 'updated_at', 'correlation_id', 'acknowledged_at']
        order_by = '-created_at'
        attrs = {
            'search': True,
            'table_actions': [],
            'row_actions': [],
        }


class LogHomeTable(ObjectTable):
    id = tables.LinkColumn(
        'log_detail',
        args=[tables.A('pk')],
    )
    acknowledged = GreenBooleanColumn(orderable=True, verbose_name=_('Ack'), attrs={'td': {'class': 'text-center'}})
    severity = SeverityAllColumn(orderable=True, verbose_name=_('Sev'), attrs={'td': {'class': 'text-center'}})
    created_at = tables.DateColumn(orderable=True, format='Y-m-d H:i')

    class Meta:
        model = Log
        sequence = ['id', 'severity', 'type', '...']
        exclude = ['select', 'source', 'task', 'updated_at']
        attrs = {
            'table_actions': [],
            'row_actions': [],
        }
