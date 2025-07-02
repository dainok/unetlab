"""Define ORM models for logs."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


class JobStatusChoices(models.TextChoices):
    """Job status."""

    CREATED = "CREATED", _("Created")
    RUNNING = "RUNNING", _("Running")
    SUCCEEDED = "SUCCEEDED", _("Succeeded")
    FAILED = "FAILED", _("Failed")
    CANCELED = "CANCELED", _("Canceled")


class LogSeverityChoices(models.IntegerChoices):
    """Log severity mapped to Django messages."""

    ERROR = messages.ERROR  # 40
    WARNING = messages.WARNING  # 30
    INFO = messages.INFO  # 20
    DEBUG = messages.DEBUG  # 10


class LogTypeChoices(models.TextChoices):
    """Log type."""

    APP = "APP", _("App")
    HOST = "HOST", _("Host")
    NODE = "NODE", _("Node")
    SCHEDULER = "SCHEDULER", _("Scheduler")


class Job(models.Model):
    """Model for Job."""

    status = models.CharField(
        null=False,
        blank=False,
        default=JobStatusChoices.CREATED.value,
        help_text="Current status of the job.",
        verbose_name="Status",
        max_length=256,
        choices=JobStatusChoices,
        editable=False,
    )
    user = models.CharField(
        null=False,
        blank=False,
        help_text="User who started the job.",
        verbose_name="Owner",
        max_length=256,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        db_table = "jobs"
        ordering = ["-created_at"]
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return str(self.pk)

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("job-detail-view", args=[str(self.pk)])


class Log(models.Model):
    """Model for Log."""

    acknowledged = models.BooleanField(
        default=False,
        help_text="True if log has been acknowledged.",
        verbose_name="Acknowledged",
    )  # True if the log has been acknowledged.
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="logs"
    )  # Associated job
    message = models.TextField(
        null=False,
        blank=False,
        editable=False,
        help_text="Log message.",
        verbose_name="Message",
    )
    severity = models.IntegerField(
        null=False,
        blank=False,
        help_text="Log severity.",
        verbose_name="Severity",
        choices=LogSeverityChoices,
        editable=False,
    )
    source = models.CharField(
        null=False,
        blank=False,
        help_text="Source of the log.",
        verbose_name="Source",
        max_length=256,
        editable=False,
    )
    type = models.CharField(
        null=False,
        blank=False,
        help_text="Type of the log.",
        verbose_name="Type",
        max_length=256,
        choices=LogTypeChoices,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Database metadata."""

        db_table = "logs"
        ordering = ["-created_at"]
        verbose_name = "Log"
        verbose_name_plural = "Logs"

    def __str__(self):
        """Return a human readable name when the object is printed."""
        return str(self.pk)

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("log-detail-view", args=[str(self.pk)])
