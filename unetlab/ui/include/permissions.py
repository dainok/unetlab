"""Custom permissions for REST API views.

Defines reusable permission classes to restrict access based on user roles.
"""

from rest_framework.permissions import BasePermission
from ui.include import messages


class IsAdminOrStaff(BasePermission):
    """Allow access only to staff or admin users.

    Attributes:
        message (str): Message returned when permission is denied.
    """

    message = messages.PERMISSION_STAFF

    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_superuser)


class IsAdmin(BasePermission):
    """Allow access only to admin (superuser) users.

    Attributes:
        message (str): Message returned when permission is denied.
    """

    message = messages.PERMISSION_ADMIN

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class ObjectPermission(BasePermission):
    """DRF permission class using the shared policy_class policy."""

    def has_permission(self, request, view):
        """List/create permissions, called before accessing the queryset."""
        policy_class = getattr(view, "policy_class")
        policy = policy_class()
        user = request.user
        method = request.method
        return policy.can(user, method, None)

    def has_object_permission(self, request, view, obj):
        """Permissions for single-object operations."""
        policy_class = getattr(view, "policy_class")
        policy = policy_class()
        user = request.user
        method = request.method
        return policy.can(user, method, obj)
