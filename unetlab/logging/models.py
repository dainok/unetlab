"""Define ORM models for Proxmox hosts."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class LogSeverityChoices(models.IntegerChoices):
    """
    Log severity.

    https://en.wikipedia.org/wiki/Syslog
    """

    EMERGENCY = 0
    ALERT = 1
    CRITICAL = 2
    ERROR = 3
    WARNING = 4
    NOTICE = 5
    INFORMATIONAL = 6
    DEBUG = 7


class LogTypeChoices(models.TextChoices):
    """Log type."""

    HOST = "HOST", _("Host")
    NODE = "NODE", _("Node")


class Log(models.Model):
    """Model for Log."""

    acknowledged = models.BooleanField(
        default=False,
        help_text="True if log has been acknowledged.",
        verbose_name="Acknowledged",
    )  # True if the log has been acknowledged.
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
    user = models.CharField(
        null=False,
        blank=False,
        help_text="User who generated the log.",
        verbose_name="User",
        max_length=256,
        editable=False,
        null=True,
        blank=True,
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
        return self.pk

    def get_absolute_url(self):
        """Return the absolute url."""
        return reverse("log-detail-view", args=[str(self.pk)])
