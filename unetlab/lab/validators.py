"""Validators for Lab app."""

import yaml
import jsonschema
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def HLDValidator(value):
    """Verify value is a valid HLD."""
    schema = str(settings.BASE_DIR / "lab" / "schema" / "hld.json")
    if value in (None, ""):
        # Use the default model behaviour
        return
    try:
        yaml.safe_load(value)
    except yaml.YAMLError:
        raise ValidationError(_("Must be a valid YAML."))

    try:
        jsonschema.validate(instance=value, schema=schema)
    except jsonschema.exceptions.ValidationError:
        raise ValidationError(_("Must be a valid HLD."))
