"""App configuration."""

from django.apps import AppConfig


class UNetLabConfig(AppConfig):
    """Config for UNetLab Django app."""

    name = "unetlab"
    verbose_name = "UNetLab"

    def ready(self):
        """Registering signals."""
        from . import signals  # noqa: F401
