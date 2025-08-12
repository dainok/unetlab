"""App configuration."""

from django.apps import AppConfig


class LabConfig(AppConfig):
    """Config for Templates management app."""

    name = "lab"  # Python path to the app
    verbose_name = "Labs"  # Human-readable app name
