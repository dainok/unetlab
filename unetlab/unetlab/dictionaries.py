"""Dictionaries.

Group all dictionaries used in UNetLab.
"""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from utilities.choices import ChoiceSet


class LogSeverityChoices(ChoiceSet):
    """
    Log severity.

    https://en.wikipedia.org/wiki/Syslog
    """

    CHOICES = [
        (0, "Emergency"),
        (1, "Alert"),
        (2, "Critical"),
        (3, "Error"),
        (4, "Warning"),
        (5, "Notice"),
        (6, "Informational"),
        (7, "Debug"),
    ]
