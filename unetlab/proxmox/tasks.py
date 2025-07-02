"""Proxmox tasks."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from celery import shared_task
from proxmoxer import ProxmoxAPI
from proxmoxer.core import ResourceException
from requests.exceptions import ConnectTimeout, ConnectionError, RequestException
from constance import config
from unetlab import messages
from proxmox.models import ProxmoxHost
from job.models import Job, JobStatusChoices
from job.utils import log


def call_proxmox_api(func, *, job_id=None):
    """Wrapper to ProxmoxAPI with error and log management."""
    try:
        return func()
    except ResourceException as err:
        log(
            job_id,
            f"{messages.proxmox_api_error} ({err.status_message.lower()})",
            40,
            "SCHEDULER",
        )
    except ConnectTimeout:
        log(job_id, f"{messages.proxmox_api_error} (timeout)", 40, "SCHEDULER")
    except ConnectionError:
        log(job_id, f"{messages.proxmox_api_error} (connection error)", 40, "SCHEDULER")
    except RequestException:
        log(job_id, f"{messages.proxmox_api_error} (exception)", 40, "SCHEDULER")


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
    log(job_obj.pk, messages.proxmox_task_rescan_started, 20, "SCHEDULER")
    job_obj.status = JobStatusChoices.RUNNING.value
    job_obj.save()

    # Get data via API
    data = call_proxmox_api(lambda: proxmox.cluster.status.get(), job_id=job_obj.pk)

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
    log(job_obj.pk, messages.proxmox_task_rescan_completed, 20, "SCHEDULER")
    job_obj.status = JobStatusChoices.SUCCEEDED.value
    job_obj.save()


def do_rescan(user=None):
    """Rescan Proxmox infrastructure."""
    # Create job and log
    job_obj = Job.objects.create(user=user)
    log(job_obj.pk, messages.proxmox_task_rescan_enqueued, 20, "APP")
    job_rescan.delay(job_obj.pk)
