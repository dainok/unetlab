"""Common regular expression validators for model fields."""

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

AlphanumericPhraseValidator = RegexValidator(
    regex=r"^[a-zA-Z0-9 ]+$",
    message=_("This field may only contain alphanumeric characters and spaces."),
)

AlphanumericValidator = RegexValidator(
    regex=r"^[a-zA-Z0-9]+$",
    message=_("This field may only contain alphanumeric characters."),
)

SimplePasswordValidator = RegexValidator(
    regex=r"^[a-zA-Z0-9 ._\-!?@#&]+$",
    message=_("Only letters, numbers, spaces, and common punctuation are allowed."),
)

VersionValidator = RegexValidator(
    regex=r"^[a-zA-Z0-9\-.]+$",
    message=_("Only letters, numbers, dots, and hyphens are allowed."),
)
