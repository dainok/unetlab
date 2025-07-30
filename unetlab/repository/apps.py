"""App configuration."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from django.apps import AppConfig


class RepositoryConfig(AppConfig):
    """Config for Repositories management app."""

    name = "repository"  # Python path to the app
    verbose_name = "Repositories"  # Human-readable app name
