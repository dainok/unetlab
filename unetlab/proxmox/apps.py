"""App configuration."""

__author__ = 'Andrea Dainese'
__contact__ = 'andrea@adainese.it'
__copyright__ = 'Copyright 2024, Andrea Dainese'
__license__ = 'GPLv3'

from django.apps import AppConfig


class ProxmoxConfig(AppConfig):
    """Config for Proxmox hosts management app."""

    name = 'proxmox'  # Python path to the app
    verbose_name = 'Proxmox'  # Human-readable app name
