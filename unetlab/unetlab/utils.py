"""Utilities."""


def db_fields_to_dict(fields):
    """Transform Model._meta.fields to dict."""
    output = {}
    for field in fields:
        output[field.name] = field.verbose_name
    return output
