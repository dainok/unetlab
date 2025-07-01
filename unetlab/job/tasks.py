"""Job tasks."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2025, Andrea Dainese"
__license__ = "GPLv3"

import redis
from celery import shared_task
from django.conf import settings
from unetlab import messages
from .models import Job, Log, LogSeverityChoices, LogTypeChoices, JobStatusChoices

@shared_task
def job_cancel_stale_jobs():
    redis_client = redis.Redis.from_url(settings.CELERY_BROKER_URL)
    if redis_client.llen(settings.CELERY_TASK_DEFAULT_QUEUE) == 0:
        # No running jobs
        job_objs = Job.objects.exclude(status="created")
        log_data = {
            "message": messages.job_task_canceled,
            "severity": LogSeverityChoices.ERROR.value,
            "source": settings.SOURCE,
            "type": LogTypeChoices.SCHEDULER.value,
        }
        # Adding logs for stale jobs
        logs = [Log(job=job_obj, **log_data) for job_obj in job_objs]
        Log.objects.bulk_create(logs)
        # Marking jobs as canceled
        job_objs.update(state=JobStatusChoices.CANCELED.value)
