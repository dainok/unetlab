import django_tables2 as tables
from job.models import Log, Job
from ui.tables import GreenBooleanColumn, SeverityAllColumn
from unetlab import messages


class JobTable(tables.Table):
    severity = SeverityAllColumn(
        orderable=True, verbose_name="Sev", attrs={"td": {"class": "text-center"}}
    )
    created_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        model = Job
        sequence = ["id", "severity", "acknowledged", "type", "..."]
        exclude = ["select"]
        attrs = {
            "title": messages.TABLE_JOB_TITLE,
            "description": messages.TABLE_JOB_DESCRIPTION,
            "detail_view": "job_detail",
            "search": True,
        }


class LogTable(tables.Table):
    acknowledged = GreenBooleanColumn(
        orderable=True, verbose_name="Ack", attrs={"td": {"class": "text-center"}}
    )
    severity = SeverityAllColumn(
        orderable=True, verbose_name="Sev", attrs={"td": {"class": "text-center"}}
    )
    created_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        model = Log
        sequence = ["id", "severity", "acknowledged", "type", "..."]
        exclude = ["select", "source", "job", "updated_at"]
        attrs = {
            "title": messages.TABLE_LOG_TITLE,
            "description": messages.TABLE_LOG_DESCRIPTION,
            "detail_view": "log_detail",
            "search": True,
        }
