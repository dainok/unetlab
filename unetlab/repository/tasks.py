"""Proxmox tasks."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

import os
import requests
from celery import shared_task
from proxmoxer import ProxmoxAPI
from proxmoxer.core import ResourceException
from requests.exceptions import ConnectTimeout, ConnectionError, RequestException
from constance import config
from ui import messages
from repository.models import Repository
from node.models import NodeTemplate
from job.models import Job, JobStatusChoices
from job.utils import log
from constance import config


@shared_task
def job_rescan(job_id):
    """Async job via Celery."""
    job_obj = Job.objects.get(pk=job_id)

    # Start the job
    log(job_obj.pk, messages.PROXMOX_TASK_RESCAN_STARTED, 20, "SCHEDULER")
    job_obj.status = JobStatusChoices.RUNNING.value
    job_obj.save()

    # Add default repositories
    unetlab_repo, created = Repository.objects.get_or_create(name="unetlab")
    if (
        unetlab_repo.uri
        != "https://raw.githubusercontent.com/dainok/unetlab/refs/heads/master/repositories/unetlab-official.json"
    ):
        unetlab_repo.uri = "https://raw.githubusercontent.com/dainok/unetlab/refs/heads/master/repositories/unetlab-official.json"
        unetlab_repo.save()
    local_repo, created = Repository.objects.get_or_create(name="local")
    if local_repo != "":
        local_repo.uri = config.TEMPLATE_DIR
        local_repo.save()

    # Scanning remote repositories
    for repo_obj in Repository.objects.filter(is_enabled=True):
        if repo_obj.name == "local":
            # Local repository
            # Create local template dir
            os.makedirs(os.path.dirname(config.TEMPLATE_DIR), exist_ok=True)

        else:
            # Remote repository
            req = requests.get(repo_obj.uri)
            if not req.ok:
                log(
                    job_obj.pk,
                    f"Failed to retrieve {repo_obj.name} repository",
                    30,
                    "SCHEDULER",
                )
                continue

            data = req.json()
            templates = data.get("templates") or list
            for template in templates:
                template_obj, created = NodeTemplate.objects.get_or_create(
                    repository=repo_obj,
                    vendor=template["vendor"],
                    os=template["os"],
                    version=template["version"],
                    extra=template["extra"],
                )
                template_obj.checksum = template["checksum"]
                template_obj.cpu = template["cpu"]
                template_obj.ram = template["ram"]
                template_obj.nics = template["nics"]
                template_obj.mgmt = template["mgmt"]
                template_obj.disks = template["disks"]
                template_obj.username = template["username"]
                template_obj.password = template["password"]
                template_obj.save()

    # End the job
    log(job_obj.pk, messages.PROXMOX_TASK_RESCAN_COMPLETED, 20, "SCHEDULER")
    job_obj.status = JobStatusChoices.SUCCEEDED.value
    job_obj.save()


def do_rescan(username=None):
    """Rescan repositories."""
    # Create job and log
    job_obj = Job.objects.create(username=username)
    log(job_obj.pk, messages.PROXMOX_TASK_RESCAN_ENQUEUED, 20, "APP")
    job_rescan.delay(job_obj.pk)
