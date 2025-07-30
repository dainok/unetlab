"""App configuration."""

from django.apps import AppConfig


class NodeConfig(AppConfig):
    """Config for Templates management app."""

    name = "node"  # Python path to the app
    verbose_name = "Nodes"  # Human-readable app name

    def ready(self):
        """
        Hook method for application startup.

        Import and register signals to ensure they are connected
        when the app is loaded by Django.
        """
        from node import signals  # noqa: F401 (import used for side effects only)
