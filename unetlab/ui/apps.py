"""Django application configuration for the UI app."""

from django.apps import AppConfig


class UNetLabConfig(AppConfig):
    """Application configuration for the `ui` app."""

    name = "ui"  # Python path to the app
    verbose_name = "User Interface"  # Human-readable app name
