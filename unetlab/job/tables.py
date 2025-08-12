import django_tables2 as tables
from job.models import Log, Job
from ui.tables import GreenBooleanColumn, SeverityAllColumn
from ui import messages


class JobTable(tables.Table):
    id = tables.LinkColumn(
        "job_detail",
        args=[tables.A("pk")],
    )
    log_count = tables.Column(
        orderable=False, verbose_name="Logs", attrs={"td": {"class": "text-center"}}
    )
    created_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")
    updated_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        model = Job
        sequence = ["id", "username", "status", "log_count", "..."]
        fields = [f.name for f in Job._meta.fields] + ["log_count"]
        exclude = ["select"]
        order_by = "-created_at"
        attrs = {
            "title": messages.TABLE_JOB_TITLE,
            "description": messages.TABLE_JOB_DESCRIPTION,
            "detail_view": "job_detail",
            "search": True,
        }


class LogTable(tables.Table):
    id = tables.LinkColumn(
        "log_detail",
        args=[tables.A("pk")],
    )
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
        order_by = "-created_at"
        attrs = {
            "title": messages.TABLE_LOG_TITLE,
            "description": messages.TABLE_LOG_DESCRIPTION,
            "detail_view": "log_detail",
            "search": True,
        }


class LogHomeTable(tables.Table):
    severity = SeverityAllColumn(
        orderable=True, verbose_name="Sev", attrs={"td": {"class": "text-center"}}
    )
    created_at = tables.DateColumn(orderable=True, format="Y-m-d H:i")

    class Meta:
        model = Log
        sequence = ["id", "severity", "type", "..."]
        exclude = ["select", "source", "job", "updated_at"]
        attrs = {
            "title": messages.TABLE_LOG_TITLE,
            "detail_view": "log_detail",
            "search": False,
        }
