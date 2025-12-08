"""Validators for Lab app."""

import yaml
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def HLDValidator(value):
    """Verify value is a valid HLD."""
    if value in (None, ""):
        # Use the default model behaviour
        return
    try:
        yaml.safe_load(value)
    except yaml.YAMLError:
        raise ValidationError(_("Must be a valid YAML."))

    