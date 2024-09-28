"""Schema validation for Log."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

from unetlab import dictionaries


def schema():
    """Return the JSON schema to validate Log data."""
    return {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
            },
            "severity": {
                "type": "integer",
                "enum": dictionaries.LogSeverityChoices.values,
            },
            "source": {
                "type": "string",
            },
            "type": {
                "type": "string",
                "enum": dictionaries.LogTypeChoices.values,
            },
            "user": {
                "type": "string",
            },
        },
        "required": [
            "message",
            "severity",
            "source",
            "type",
        ],
    }
