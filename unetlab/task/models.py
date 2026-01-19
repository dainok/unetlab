"""Define ORM models for Task app."""

import uuid
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ui.include.validators import PhraseValidator


#############################################################################
# Task
#############################################################################


class TaskStatusChoices(models.TextChoices):
    """Enumeration for Task status."""

    CREATED = 'CREATED', _('Created')
    RUNNING = 'RUNNING', _('Running')
    SUCCEEDED = 'SUCCEEDED', _('Succeeded')
    FAILED = 'FAILED', _('Failed')
    CANCELED = 'CANCELED', _('Canceled')


class Task(models.Model):
    """Model for background Task."""

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        validators=[PhraseValidator],
        help_text=_('Task name.'),
    )
    status = models.CharField(
        max_length=32,
        choices=TaskStatusChoices.choices,
        default=TaskStatusChoices.CREATED,
        verbose_name=_('Status'),
        help_text=_('Current status of the task.'),
        editable=False,
        db_index=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tasks',
        help_text=_('User who started the task.'),
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        db_table = 'tasks'
        ordering = ['-created_at']
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.pk

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse('task-detail-view', args=[str(self.pk)])

    def mark_canceled(self):
        """Proceed a Task from created/running to canceled."""
        if self.status in (TaskStatusChoices.CREATED, TaskStatusChoices.RUNNING):
            return
        self.status = TaskStatusChoices.CANCELED
        self.save(update_fields=["status", "updated_at"])

    def mark_failed(self):
        """Proceed a Task from created/running to failed."""
        if self.status in (TaskStatusChoices.CREATED, TaskStatusChoices.RUNNING):
            return
        self.status = TaskStatusChoices.FAILED
        self.save(update_fields=["status", "updated_at"])

    def mark_running(self):
        """Proceed a Task from created to running."""
        if self.status != TaskStatusChoices.CREATED:
            return
        self.status = TaskStatusChoices.RUNNING
        self.save(update_fields=["status", "updated_at"])

    def mark_succeeded(self):
        """Proceed a Task from running to succeeded."""
        if self.status != TaskStatusChoices.RUNNING:
            return
        self.status = TaskStatusChoices.SUCCEEDED
        self.save(update_fields=["status", "updated_at"])


#############################################################################
# Log
#############################################################################


class LogSeverityChoices(models.IntegerChoices):
    """Enumeration for log severity. Uses integers as per django.contrib.messages constants."""

    ERROR = 40, _('Error')
    WARNING = 30, _('Warning')
    INFO = 20, _('Info')
    DEBUG = 10, _('Debug')


class LogTypeChoices(models.TextChoices):
    """Enumeration for log types/categories."""

    APP = 'APP', _('App')
    HOST = 'HOST', _('Host')
    NODE = 'NODE', _('Node')
    SCHEDULER = 'SCHEDULER', _('Scheduler')
    UI = 'UI', _('UI')


class Log(models.Model):
    """Model representing a Logb."""

    acknowledged = models.BooleanField(
        default=False,
        verbose_name=_('Acknowledged'),
        help_text=_('True if the log has been acknowledged.'),
        db_index=True,
    )
    correlation_id = models.UUIDField(
        default=uuid.uuid4,
        db_index=True,
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='logs',
        verbose_name=_('Task'),
        help_text=_('Task associated with this log.'),
    )
    message = models.TextField(
        verbose_name=_('Message'),
        help_text=_('Log message content.'),
        editable=False,
    )
    severity = models.IntegerField(
        choices=LogSeverityChoices.choices,
        verbose_name=_('Severity'),
        help_text=_('Severity level of the log.'),
        editable=False,
        db_index=True,
    )
    hostname = models.CharField(
        max_length=255,
        verbose_name=_('Hostname'),
        help_text=_('Hostname generating the log.'),
        editable=False,
        db_index=True,
    )
    type = models.CharField(
        max_length=255,
        choices=LogTypeChoices.choices,
        verbose_name=_('Type'),
        help_text=_('Type/category of the log.'),
        editable=False,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    acknowledged_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        db_table = 'logs'
        ordering = ['-created_at']
        verbose_name = _('Log')
        verbose_name_plural = _('Logs')
        indexes = [
            models.Index(fields=['task', 'severity']),
            models.Index(fields=['task', 'created_at']),
        ]

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return self.pk

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse('task-detail-view', args=[str(self.pk)])
