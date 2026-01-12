"""Custom permissions for REST API views."""

from rest_framework.permissions import BasePermission


class ObjectPermission(BasePermission):
    """DRF permission class using the shared policy_class policy."""

    def get_payload(self, request):
        """Given a request, return the payload."""
        payload = {}
        if request.content_type == 'application/json':
            # DRF
            return request.data
        elif request.content_type.startswith('multipart/form-data'):
            # HTML
            payload = {k: v[0] if len(v) == 1 else v for k, v in request.POST.lists()}

        return payload

    def has_permission(self, request, view):
        """List/create permissions, called before accessing the queryset (DRF only)."""
        policy_class = getattr(view, 'policy_class')
        policy = policy_class()
        user = request.user
        method = request.method
        payload = self.get_payload(request)

        return policy.can(user, method, None, payload)

    def has_object_permission(self, request, view, obj):
        """Permissions for single-object operations (DRF only)."""
        policy_class = getattr(view, 'policy_class')
        policy = policy_class()
        user = request.user
        method = request.method
        payload = self.get_payload(request)

        return policy.can(user, method, obj, payload)
