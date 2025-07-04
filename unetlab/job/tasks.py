"""Celery job tasks for UNetLab.

These background tasks handle periodic operations related to job management,
such as canceling stale jobs that were never picked up by Celery workers.
"""

import redis
from celery import shared_task
from django.conf import settings

from unetlab import messages
from job.models import Job, JobStatusChoices
from job.utils import log


@shared_task
def job_cancel_stale_jobs():
    """
    Cancel stale jobs that are stuck in CREATED or RUNNING state but are
    no longer being processed by any active Celery worker.

    This task is intended to be run periodically (e.g., via Celery Beat).
    It checks if the task queue is empty and, if so, assumes that jobs are stale.
    """
    # Connect to Redis using the configured Celery broker URL
    redis_client = redis.Redis.from_url(settings.CELERY_BROKER_URL)

    # Check if the default Celery task queue is empty
    if redis_client.llen(settings.CELERY_TASK_DEFAULT_QUEUE) == 0:
        # Fetch all jobs that were never processed or stuck mid-process
        stale_job_qs = Job.objects.filter(
            status__in=[JobStatusChoices.CREATED, JobStatusChoices.RUNNING]
        )
        stale_job_ids = list(stale_job_qs.values_list("id", flat=True))

        if stale_job_ids:
            # Log the cancellation for each stale job
            for job_id in stale_job_ids:
                log(
                    job_id=job_id,
                    message=messages.JOB_TASK_CANCELED,
                    severity=40,
                    source="SCHEDULER",
                )

            # Bulk update all stale jobs in a single query
            stale_job_qs.update(status=JobStatusChoices.CANCELED.value)
