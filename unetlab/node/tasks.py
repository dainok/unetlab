"""Proxmox connector."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

import socket

# from proxmoxer import ProxmoxAPI

import django_rq

from unetlab import dictionaries
from unetlab import models


def save_log(log):
    """Save a log."""
    print("*** SAVE A LOG")
    # TODO: Validate the log
    models.Log.objects.create(**log)


def delete(host=None, node_id=None):
    """Delete a stopped node."""
    print("DELETE")
    source = socket.gethostname().lower()
    type = dictionaries.LogTypeChoices.HOST.value
    user = None

    severity = dictionaries.LogSeverityChoices.NOTICE.value
    message = "Ciao"

    log = {
        "source": source,
        "type": type,
        "user": user,
        "severity": severity,
        "message": message,
    }

    queue = django_rq.get_queue("logs")
    queue.enqueue(save_log, log)


def provision(
    host=None, template_id=None, node_id=None, node_name=None, interface_count=0
):
    """Provision a node from a template."""
    print("PROVISION")
    pass


def reboot(host=None, node_id=None):
    """Graceful restart a node."""
    print("REBOOT")
    pass


def reset(host=None, node_id=None):
    """Force a reset of a node."""
    print("RESET")
    pass


def shutdown(host=None, node_id=None):
    """Graceful shutdown a node."""
    print("SHUTDOWN")
    pass


def start(host=None, node_id=None):
    """Start a node."""
    print("START")
    print(f"{node_id} ON {host}")
    pass


def stop(host=None, node_id=None):
    """Stop a node."""
    print("STOP")
    pass


def suspend(host=None, node_id=None):
    """Suspend a node."""
    print("SUSPEND")
    pass
