"""Job tasks."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2025, Andrea Dainese"
__license__ = "GPLv3"

import redis
from celery import shared_task
from django.conf import settings
from unetlab import messages
from job.models import Job, JobStatusChoices
from job.utils import log


@shared_task
def job_cancel_stale_jobs():
    """Set as canceled jobs which are created but no Celery is running."""
    redis_client = redis.Redis.from_url(settings.CELERY_BROKER_URL)
    if redis_client.llen(settings.CELERY_TASK_DEFAULT_QUEUE) == 0:
        # No running jobs
        job_qs = Job.objects.filter(
            status__in=[JobStatusChoices.CREATED, JobStatusChoices.RUNNING]
        )
        # Adding logs for stale jobs
        for job_obj in job_qs:
            log(job_obj.pk, messages.JOB_TASK_CANCELED, 40, "SCHEDULER")
        # Marking jobs as canceled
        job_qs.update(status=JobStatusChoices.CANCELED.value)
