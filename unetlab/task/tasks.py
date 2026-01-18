"""Celery tasks for Task app."""

import redis
from celery import shared_task
from django.conf import settings

from ui.include import messages
from task.models import Task, TaskStatusChoices
from task.utils import log


@shared_task
def cancel_stale_tasks():
    """
    Cancel stale tasks that are stuck in CREATED or RUNNING state but are
    no longer being processed by any active Celery worker.

    This task is intended to be run periodically (see settings.CELERY_BEAT_SCHEDULE).
    It checks if the task queue is empty and, if so, assumes that tasks are stale.
    """
    # Connect to Redis using the configured Celery broker URL
    redis_client = redis.Redis.from_url(settings.CELERY_BROKER_URL)

    # Check if the default Celery task queue is empty
    if redis_client.llen(settings.CELERY_TASK_DEFAULT_QUEUE) == 0:
        # Fetch all tasks that were never processed or stuck mid-process
        stale_task_qs = Task.objects.filter(status__in=[TaskStatusChoices.CREATED, TaskStatusChoices.RUNNING])
        stale_task_ids = list(stale_task_qs.values_list('id', flat=True))

        if stale_task_ids:
            # Log the cancellation for each stale task
            for task_id in stale_task_ids:
                log(
                    task_id=task_id,
                    message=messages.task_TASK_CANCELED,
                    severity=40,
                    source='SCHEDULER',
                )

            # Bulk update all stale tasks in a single query
            stale_task_qs.update(status=TaskStatusChoices.CANCELED.value)
