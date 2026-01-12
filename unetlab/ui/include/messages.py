"""Centralized, user-facing messages for UNetLab.

This module defines all the standardized messages used across
the UI, API responses, and tables, to ensure consistency.
"""

from django.utils.translation import gettext_lazy as _


#############################################################################
# General choices
#############################################################################


CHOICES_YES_NO = [
    ('', '---------'),
    (True, 'Yes'),
    (False, 'No'),
]


#############################################################################
# General actions
#############################################################################


ADD = _('Add')
DELETE = _('Delete')
EDIT = _('Edit')
VIEW = _('View')


#############################################################################
# Forms
#############################################################################


PASSWORD1_HELP = 'Leave blank to not change the password.'
PASSWORD2_HELP = 'Repeat password to confirm.'  # nosec B105 # not an hardcoded password
PASSWORD_ERROR = 'The passwords do not match.'  # nosec B105 # not an hardcoded password


#############################################################################
# Permissions
#############################################################################


PERMISSION_ADMIN = _('You must be an admin user to access this resource.')
PERMISSION_DENIED = _('You do not have permission to access this object.')
PERMISSION_STAFF = _('You must be a staff or admin user to access this resource.')


#############################################################################
# Validators
#############################################################################


ALPHANUMERIC_PHRASE_ERROR = _(
    'This field may only contain alphanumeric characters and spaces.'
)
ALPHANUMERIC_ERROR = _('This field may only contain alphanumeric characters.')
SIMPLE_PASSWORD_ERROR = _(
    'Only letters, numbers, spaces, and common punctuation are allowed.'
)
VERSION_ERROR = _('Only letters, numbers, dots, and hyphens are allowed.')


#############################################################################
# Table titles and descriptions
#############################################################################


TABLE_GROUP_TITLE = _('Groups')
TABLE_GROUP_DESCRIPTION = _('List of all user groups in the system.')

TABLE_JOB_TITLE = _('Jobs')
TABLE_JOB_DESCRIPTION = _('Displays all scheduled and completed jobs.')

TABLE_LAB_TITLE = _('Labs')
TABLE_LAB_DESCRIPTION = _('All available labs.')

TABLE_LABINSTANCE_TITLE = _('Running labs')
TABLE_LABINSTANCE_DESCRIPTION = _('All available lab instances.')

TABLE_LOG_TITLE = _('System Logs')
TABLE_LOG_DESCRIPTION = _('Displays all system logs with relevant details.')

TABLE_PROXMOXHOST_TITLE = _('Hosts')
TABLE_PROXMOXHOST_DESCRIPTION = _('List of all Proxmox hosts managed by the system.')

TABLE_REPOSITORY_TITLE = _('Repositories')
TABLE_REPOSITORY_DESCRIPTION = _('All configured repositories and their metadata.')

TABLE_NODETEMPLATE_TITLE = _('Templates')
TABLE_NODETEMPLATE_DESCRIPTION = _('All available templates for virtual machines.')

TABLE_TOKEN_TITLE = _('Tokens')
TABLE_TOKEN_DESCRIPTION = _('List of all registered API tokens.')

TABLE_USER_TITLE = _('Users')
TABLE_USER_DESCRIPTION = _('List of all registered users.')


#############################################################################
# Job/task messages
#############################################################################


JOB_TASK_CANCELED = _('Job was canceled due to a stale or invalid status.')

PROXMOX_TASK_RESCAN_COMPLETED = _(
    'Proxmox infrastructure rescan completed successfully.'
)
PROXMOX_TASK_RESCAN_ENQUEUED = _('Proxmox infrastructure rescan has been queued.')
PROXMOX_TASK_RESCAN_STARTED = _('Proxmox infrastructure rescan has started.')
PROXMOX_API_ERROR = _('Failed to execute the request on the Proxmox API.')


#############################################################################
# Filters
#############################################################################


FILTER_ACTIVE_USERS = _('Active users')
FILTER_ADMIN_USERS = _('Admin users')
FILTER_STAFF_USERS = _('Staff users')
FILTER_LOGGED_BEFORE = _('Last login before')
FILTER_LOGGED_AFTER = _('Last login after')


#############################################################################
# Bus messages
#############################################################################


MSG_VALUE_ERROR = _('Value error')
MSG_CONFIG_UPDATED = _('Configuration updated.')
