"""Hosts related tasks."""

from proxmoxer import ProxmoxAPI, core

from django.utils.timezone import now

from constance import config
from unetlab import models

def hosts_update():
    """Update hosts from Proxmox primary address."""
    proxmox = ProxmoxAPI(config.PROXMOX_PRIMARY_ADDRESS, user=config.PROXMOX_USERNAME, token_name=config.PROXMOX_TOKEN_ID, token_value=config.PROXMOX_SECRET, verify_ssl=config.PROXMOX_VERIFY_SSL)
    try:
        hosts_data = proxmox.nodes.get()
    except core.ResourceException:
        # TODO
        pass

    for host_data in hosts_data:
        # Get or create Host
        host_obj, created = models.Host.objects.get_or_create(name=host_data["node"])

        # Update Host
        if host_data["status"] == "online":
            host_obj.is_online = True
        else:
            host_obj.is_online = False
        host_obj.save()

    # Update timestamp
    config.PROXMOX_UPDATED_AT = now()
