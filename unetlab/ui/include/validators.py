"""Common regular expression validators for model fields.

This module provides reusable RegexValidator instances for enforcing
standardized input rules across models, forms, and serializers.
"""

from django.core.validators import RegexValidator
from ui.include import messages

AlphanumericPhraseValidator = RegexValidator(
    regex=r"^[a-zA-Z0-9 ]+$",
    message=messages.ALPHANUMERIC_PHRASE_ERROR,
)

AlphanumericValidator = RegexValidator(
    regex=r"^[a-zA-Z0-9]+$",
    message=messages.ALPHANUMERIC_ERROR,
)

VersionValidator = RegexValidator(
    regex=r"^[a-zA-Z0-9\-.]+$",
    message=messages.VERSION_ERROR,
)

SimplePasswordValidator = RegexValidator(
    regex=r"^[a-zA-Z0-9 ._\-!?@#&]+$",
    message=messages.SIMPLE_PASSWORD_ERROR,
)
