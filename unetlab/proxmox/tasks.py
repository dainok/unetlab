"""Proxmox connector."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

import socket
from log import models as log_models
import django_rq


def do_rescan(user=None):
    """Rescan Proxmox infrastructure."""
    # Log request
    log_obj = {
        "message": "Initiated Proxmox infrastructure rescan.",
        "severity": log_models.LogSeverityChoices.INFORMATIONAL.value,
        # "source": socket.gethostname().lower(),
        # "type": log_models.LogTypeChoices.HOST.value,
        "user": user,
    }
    log_models.Log.objects.create(**log_obj)

    # Enqueue action
    action = {
        
    }
    
    queue = django_rq.get_queue("logs")
    queue.enqueue(save_log, log)
