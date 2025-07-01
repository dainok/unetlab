"""Proxmox connector."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

import socket
from job import models as job_models
import django_rq


def rq_rescan(job_id):
    """Async action."""
    # End the job
    job_obj = job_models.Job.objects.get(pk=job_id)
    log_data = {
        "message": "Completed Proxmox infrastructure rescan.",
        "severity": job_models.LogSeverityChoices.INFORMATIONAL.value,
        "source": socket.gethostname().upper(),
        "type": job_models.LogTypeChoices.APP.value,
    }
    job_obj.log_set.create(**log_data)
    job_obj.status = job_models.JobStatusChoices.SUCCEEDED.value
    job_obj.save()


def do_rescan(user=None):
    """Rescan Proxmox infrastructure."""
    # Create job and log
    job_obj = job_models.Job.objects.create(user=user)
    log_data = {
        "message": "Initiated Proxmox infrastructure rescan.",
        "severity": job_models.LogSeverityChoices.INFORMATIONAL.value,
        "source": socket.gethostname().upper(),
        "type": job_models.LogTypeChoices.APP.value,
    }
    job_obj.log_set.create(**log_data)

    queue = django_rq.get_queue(job_models.LogTypeChoices.APP.value)
    queue.enqueue(rq_rescan, job_obj.pk)
