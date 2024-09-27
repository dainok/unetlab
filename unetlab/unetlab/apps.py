"""App configuration."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.apps import AppConfig


class UNetLabConfig(AppConfig):
    """Config for UNetLab Django app."""

    name = "unetlab"
    verbose_name = "UNetLab"

    def ready(self):
        """Registering signals."""
        from . import signals  # noqa: F401
