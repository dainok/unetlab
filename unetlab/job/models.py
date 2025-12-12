"""Define ORM models for logs."""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


correlation_id
Tutti i log relativi alla stessa richiesta condividono lo stesso correlation_id.
fare overload di logging per usare questa struttura dati



class JobStatusChoices(models.TextChoices):
    """Enumeration for Job status."""

    CREATED = "CREATED", _("Created")
    RUNNING = "RUNNING", _("Running")
    SUCCEEDED = "SUCCEEDED", _("Succeeded")
    FAILED = "FAILED", _("Failed")
    CANCELED = "CANCELED", _("Canceled")


class LogSeverityChoices(models.IntegerChoices):
    """
    Enumeration for log severity, mapped to Django's message levels.
    Uses integers as per django.contrib.messages constants.
    """

    ERROR = messages.ERROR  # 40
    WARNING = messages.WARNING  # 30
    INFO = messages.INFO  # 20
    DEBUG = messages.DEBUG  # 10


class LogTypeChoices(models.TextChoices):
    """Enumeration for log types/categories."""

    APP = "APP", _("App")
    HOST = "HOST", _("Host")
    NODE = "NODE", _("Node")
    SCHEDULER = "SCHEDULER", _("Scheduler")
    UI = "UI", _("UI")


class Job(models.Model):
    """Model representing a background or system Job."""

    status = models.CharField(
        max_length=255,
        choices=JobStatusChoices.choices,
        default=JobStatusChoices.CREATED,
        verbose_name=_("Status"),
        help_text=_("Current status of the job."),
        editable=False,
        db_index=True,
    )
    username = models.CharField(
        max_length=255,
        verbose_name=_("Owner"),
        help_text=_("User who started the job."),
        editable=False,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        db_table = "jobs"
        ordering = ["-created_at"]
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")

    def __str__(self) -> str:
        """Return string representation of the job (its primary key)."""
        return str(self.pk)

    def get_absolute_url(self) -> str:
        """Return absolute URL for the job detail view."""
        return reverse("job-detail-view", args=[str(self.pk)])


class Log(models.Model):
    """Model representing a log entry linked to a job."""

    acknowledged = models.BooleanField(
        default=False,
        verbose_name=_("Acknowledged"),
        help_text=_("True if the log has been acknowledged."),
        db_index=True,
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="logs",
        verbose_name=_("Job"),
        help_text=_("Job associated with this log."),
    )
    message = models.TextField(
        verbose_name=_("Message"),
        help_text=_("Log message content."),
        editable=False,
    )
    severity = models.IntegerField(
        choices=LogSeverityChoices.choices,
        verbose_name=_("Severity"),
        help_text=_("Severity level of the log."),
        editable=False,
        db_index=True,
    )
    source = models.CharField(
        max_length=255,
        verbose_name=_("Source"),
        help_text=_("Source of the log."),
        editable=False,
        db_index=True,
    )
    type = models.CharField(
        max_length=255,
        choices=LogTypeChoices.choices,
        verbose_name=_("Type"),
        help_text=_("Type/category of the log."),
        editable=False,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        db_table = "logs"
        ordering = ["-created_at"]
        verbose_name = _("Log")
        verbose_name_plural = _("Logs")

    def __str__(self) -> str:
        """Return string representation of the log (its primary key)."""
        return str(self.pk)

    def get_absolute_url(self) -> str:
        """Return absolute URL for the log detail view."""
        return reverse("log-detail-view", args=[str(self.pk)])
