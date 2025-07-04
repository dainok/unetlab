"""Utilities."""

from typing import List, Dict
from django.db.models.fields import Field


def db_fields_to_dict(fields: List[Field]) -> Dict[str, str]:
    """Transform a list of Django model fields to a dictionary mapping
    field names to their verbose names.

    Args:
        fields (List[Field]): List of Django model fields.

    Returns:
        Dict[str, str]: Dictionary with field names as keys and verbose names as values.
    """
    output = {}
    for field in fields:
        output[field.name] = str(field.verbose_name)
    return output
