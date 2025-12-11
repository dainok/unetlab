"""Validators for Lab app."""

import json
import jsonschema
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def HLDValidator(value):
    """Verify value is a valid HLD."""
    if value in (None, ""):
        # Use the default model behaviour
        return

    # Load schema
    schema_file = str(settings.BASE_DIR / "lab" / "schema" / "hld.json")
    with open(schema_file, "r") as f:
        schema = json.loads(f.read())

    # Validate HLD (JSON)
    try:
        jsonschema.validate(instance=value, schema=schema)
    except jsonschema.exceptions.ValidationError:
        raise ValidationError(_("Must be a valid HLD."))
