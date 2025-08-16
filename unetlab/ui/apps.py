"""Django application configuration for the UI app."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.apps import AppConfig


class UNetLabConfig(AppConfig):
    """Application configuration for the `ui` app.

    Defines metadata used by Django when loading the app.
    """

    name = "ui"
    verbose_name = "User Interface"
