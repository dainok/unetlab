"""Utility functions for the job app."""

from django.conf import settings
from job.models import Log, LogSeverityChoices, LogTypeChoices


def log(
    job_id: int,
    message: str,
    severity: int = LogSeverityChoices.INFO.value,
    log_type: str = LogTypeChoices.APP.value,
) -> None:
    """
    Create a log entry associated with a specific job.

    Args:
        job_id (int): ID of the job to associate the log with.
        message (str): The log message.
        severity (int, optional): Log severity level (default: INFO).
        log_type (str, optional): Type/category of the log (default: APP).

    Returns:
        None
    """
    Log.objects.create(
        job_id=job_id,
        message=message,
        severity=severity,
        source=settings.SOURCE,
        type=log_type,
    )
