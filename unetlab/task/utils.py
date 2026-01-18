"""Utility functions for the Task app."""

from django.conf import settings
from task.models import Log, LogSeverityChoices, LogTypeChoices


def log(
    task_id: int,
    message: str,
    severity: int = LogSeverityChoices.INFO.value,
    log_type: str = LogTypeChoices.APP.value,
) -> None:
    """Create a Log associated with a specific job."""
    Log.objects.create(
        task_id=task_id,
        message=message,
        severity=severity,
        source=settings.SOURCE,
        type=log_type,
    )
