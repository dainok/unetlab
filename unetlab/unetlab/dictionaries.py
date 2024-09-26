"""Dictionaries.

Group all dictionaries used in UNetLab.
"""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.db import models
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
    WEB = "WEB", _("Web")
