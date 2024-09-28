"""Schema validation for Action."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"


def schema():
    """Return the JSON schema to validate Action data."""
    return {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": [
                    "DELETE",
                    "REBOOT",
                    "RESET",
                    "SHUTDOWN",
                    "START",
                    "STOP",
                    "SUSPEND",
                ],
            },
            "id": {
                "type": "integer",
                # "enum": dictionaries.LogSeverityChoices.values,
            },
            "user": {
                "type": "string",
                # "enum": dictionaries.LogTypeChoices.values,
            },
        },
        "required": [
            "action",
            "id",
            "user",
        ],
    }
