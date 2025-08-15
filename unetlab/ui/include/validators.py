from django.core.validators import RegexValidator

AlphanumericPhraseValidator = RegexValidator(
    regex=r"^[a-zA-Z0-9 ]+$",
    message="Questo campo deve contenere solo caratteri alfanumerici.",
)

AlphanumericValidator = RegexValidator(
    regex=r"^[a-zA-Z0-9]+$",
    message="Questo campo deve contenere solo caratteri alfanumerici.",
)

VersionValidator = RegexValidator(
    regex=r"^[a-zA-Z0-9\-.]+$",
    message="Sono consentiti solo lettere, numeri, spazi, punti e trattini.",
)

SimplePasswordalidator = RegexValidator(
    regex=r"^[a-zA-Z0-9 ._\-!?@#&]+$",
    message="Sono consentiti solo lettere, numeri, spazi, punti e trattini.",
)
