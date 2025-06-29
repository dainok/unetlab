"""App configuration."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.apps import AppConfig


class UNetLabConfig(AppConfig):
    """Config for logging management app."""

    name = "logging"
    verbose_name = "Log management"
