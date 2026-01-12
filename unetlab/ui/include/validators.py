"""Common regular expression validators for model fields."""

import yaml
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


AlphanumericValidator = RegexValidator(
    regex=r'^[a-zA-Z0-9]+$',
    message=_('This field may only contain alphanumeric characters.'),
)

PhraseValidator = RegexValidator(
    regex=r'^[a-zA-Z0-9 _\-]+$',
    message=_('This field may only contain alphanumeric characters, spaces and -_.'),
)

SimplePasswordValidator = RegexValidator(
    regex=r'^[a-zA-Z0-9 ._\-!?@#&]+$',
    message=_('Only letters, numbers, spaces, and common punctuation are allowed.'),
)

VersionValidator = RegexValidator(
    regex=r'^[a-zA-Z0-9\-.]+$',
    message=_('Only letters, numbers, dots, and hyphens are allowed.'),
)


def YAMLValidator(value):
    """Verify value is a valid YAML string."""
    if value in (None, ''):
        # Use the default model behaviour
        return
    try:
        yaml.safe_load(value)
    except yaml.YAMLError:
        raise ValidationError(_('Must be a valid YAML.'))
