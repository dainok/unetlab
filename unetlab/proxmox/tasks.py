"""Proxmox tasks."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from celery import shared_task
from proxmoxer import ProxmoxAPI
from proxmoxer.core import ResourceException
from django.conf import settings
from constance import config
from unetlab import messages
from .models import ProxmoxHost
from job.models import Log, Job, LogTypeChoices, JobStatusChoices, LogSeverityChoices


def log_api_error(job_id=None, error=None, message=None):
    """Generate log with API error and debug info."""
    logs_data = [
        {
            "job_id": job_id,
            "message": f"{messages.proxmox_api_error} ({error})",
            "severity": LogSeverityChoices.ERROR.value,
            "source": settings.SOURCE,
            "type": LogTypeChoices.SCHEDULER.value,
        },
        {
            "job_id": job_id,
            "message": message,
            "severity": LogSeverityChoices.DEBUG.value,
            "source": settings.SOURCE,
            "type": LogTypeChoices.SCHEDULER.value,
        },
    ]
    logs = [Log(**log_data) for log_data in logs_data]
    Log.objects.bulk_create(logs)


@shared_task
def job_rescan(job_id):
    """Async job via Celery."""
    job_obj = Job.objects.get(pk=job_id)
    proxmox = ProxmoxAPI(
        config.PROXMOX_PRIMARY_ADDRESS,
        user=config.PROXMOX_USERNAME,
        token_name=config.PROXMOX_TOKEN_ID,
        token_value=config.PROXMOX_SECRET,
        verify_ssl=config.PROXMOX_VERIFY_SSL,
    )

    # Start the job
    log_data = {
        "message": messages.proxmox_task_rescan_started,
        "severity": LogSeverityChoices.INFO.value,
        "source": settings.SOURCE,
        "type": LogTypeChoices.APP.value,
    }
    job_obj.logs.create(**log_data)
    job_obj.status = JobStatusChoices.RUNNING.value
    job_obj.save()

    # Get data via API
    try:
        data = proxmox.cluster.status.get()
    except ResourceException as err:
        log_api_error(job_id=job_id, error=err.status_message, message=err.content)
        job_obj.status = JobStatusChoices.FAILED.value
        job_obj.save()
        return

    # Analyse data
    hosts = []
    for entry in data:
        if entry["type"] != "node":
            continue
        # Add/update ProxmoxHost
        hosts.append(entry["name"])
        host_obj, created = ProxmoxHost.objects.get_or_create(name=entry["name"])
        host_obj.ip_address = entry["ip"]
        host_obj.is_online = True
        host_obj.is_orphan = False
        host_obj.save()
    # Mark missing hosts as orphans
    ProxmoxHost.objects.exclude(name__in=hosts).update(is_orphan=True)

    # End the job
    log_data = {
        "message": messages.proxmox_task_rescan_completed,
        "severity": LogSeverityChoices.INFO.value,
        "source": settings.SOURCE,
        "type": LogTypeChoices.APP.value,
    }
    job_obj.logs.create(**log_data)
    job_obj.status = JobStatusChoices.SUCCEEDED.value
    job_obj.save()


def do_rescan(user=None):
    """Rescan Proxmox infrastructure."""
    # Create job and log
    job_obj = Job.objects.create(user=user)
    log_data = {
        "message": messages.proxmox_task_rescan_enqueued,
        "severity": LogSeverityChoices.INFO.value,
        "source": settings.SOURCE,
        "type": LogTypeChoices.APP.value,
    }
    job_obj.logs.create(**log_data)
    job_rescan.delay(job_obj.pk)
