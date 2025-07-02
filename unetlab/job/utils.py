"""Utilities."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2025, Andrea Dainese"
__license__ = "GPLv3"

from django.conf import settings
from job.models import Log, LogSeverityChoices, LogTypeChoices


def log(
    job_id: int,
    message: str,
    severity: int = LogSeverityChoices.INFO.value,
    log_type: str = LogTypeChoices.APP.value,
) -> None:
    """Shortcut to add a log."""
    Log.objects.create(
        job_id=job_id,
        message=message,
        severity=severity,
        source=settings.SOURCE,
        type=log_type,
    )
