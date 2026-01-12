"""Django application configuration for the UI app."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UNetLabConfig(AppConfig):
    """Application configuration for the UI app."""

    name = 'ui'  # Python path to the app
    verbose_name = _('User Interface')  # Human-readable app name
