"""Custom permissions for REST API views."""

from rest_framework.permissions import BasePermission


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
