"""Dictionaries.

Group all dictionaries used in UNetLab.
"""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.db import models


class LogSeverityChoices(models.IntegerChoices):
    """
    Log severity.

    https://en.wikipedia.org/wiki/Syslog
    """

    Emergency = 0
    Alert = 1
    Critical = 2
    Error = 3
    Warning = 4
    Notice = 5
    Informational = 6
    Debug = 7
