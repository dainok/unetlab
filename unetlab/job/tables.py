import django_tables2 as tables
from django.conf import settings
from job.models import Log, Job
from unetlab.tables import GreenBooleanColumn

from django.core.paginator import Paginator

class LogTable(tables.Table):
    acknowledged = GreenBooleanColumn(orderable=True, verbose_name="Ack", attrs={"td": {"class": "text-center"}})
    created_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        model = Log
        exclude = ["select", "source", "job", "updated_at"]

