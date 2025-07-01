"""Utilities."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2025, Andrea Dainese"
__license__ = "GPLv3"

from django.conf import settings
from .models import Log, LogSeverityChoices, LogTypeChoices

def log(job_id, message, severity=LogSeverityChoices.INFO.value, log_type=LogTypeChoices.APP.value):
    Log.objects.create(
        job_id = job_id,
        message=message,
        severity=severity,
        source=settings.SOURCE,
        type=log_type,
    )
