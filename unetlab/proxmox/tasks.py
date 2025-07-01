"""Proxmox tasks."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from celery import shared_task
from django.conf import settings
from unetlab import messages
from job.models import Job, LogTypeChoices, JobStatusChoices, LogSeverityChoices


@shared_task
def job_rescan(job_id):
    """Async job via Celery."""
    # End the job
    job_obj = Job.objects.get(pk=job_id)
    log_data = {
        "message": messages.proxmox_task_rescan_completed,
        "severity": LogSeverityChoices.INFO.value,
        "source": settings.SOURCE,
        "type": LogTypeChoices.APP.value,
    }
    job_obj.log_set.create(**log_data)
    job_obj.status = JobStatusChoices.SUCCEEDED.value
    job_obj.save()


def do_rescan(user=None):
    """Rescan Proxmox infrastructure."""
    # Create job and log
    job_obj = Job.objects.create(user=user)
    log_data = {
        "message": messages.proxmox_task_rescan_started,
        "severity": LogSeverityChoices.INFO.value,
        "source": settings.SOURCE,
        "type": LogTypeChoices.APP.value,
    }
    job_obj.log_set.create(**log_data)
    job_rescan.delay(job_obj.pk)
