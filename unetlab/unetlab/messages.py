"""Centralized user-facing messages for UNetLab."""

from django.utils.translation import gettext_lazy as _

# Generic job/task messages
JOB_TASK_CANCELED = _("Job canceled due to stale status.")

# Proxmox messages (grouped by context)
PROXMOX_TASK_RESCAN_COMPLETED = _(
    "Proxmox infrastructure rescan completed successfully."
)
PROXMOX_TASK_RESCAN_ENQUEUED = _("Proxmox infrastructure rescan enqueued.")
PROXMOX_TASK_RESCAN_STARTED = _("Proxmox infrastructure rescan initiated.")
PROXMOX_API_ERROR = _("Proxmox API request failed.")

# Permissions
PERMISSION_ADMIN = _("You must be a staff or admin user to access this resource.")
