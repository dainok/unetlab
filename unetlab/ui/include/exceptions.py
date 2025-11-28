from django.core.exceptions import PermissionDenied


class NotAuthenticated(PermissionDenied):
    """Raised when user is not authenticated (401)."""

    status_code = 401
