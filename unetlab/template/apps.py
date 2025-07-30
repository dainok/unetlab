"""App configuration."""

from django.apps import AppConfig


class UNetLabConfig(AppConfig):
    """Config for Templates management app."""

    name = "template"
    verbose_name = "Templates"

    def ready(self):
        """
        Hook method for application startup.

        Import and register signals to ensure they are connected
        when the app is loaded by Django.
        """
        from template import signals  # noqa: F401 (import used for side effects only)
