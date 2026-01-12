"""Permissions for Node app."""

#############################################################################
# NodeTemplate
#############################################################################


class NodeTemplatePermissionPolicy:
    """UI and DRF (API) permisson policy for NodeTemplate objects."""

    def can(self, user, method, target=None):
        """Defines what the requesting user can do based on their role and HTTP method."""

        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest users are not allowed to do anything
            return None

        # === COMMON RULES ===
        if not target and method in (
            'GET',
            'OPTIONS',
            'HEAD',
            'PUT',
            'PATCH',
            'DELETE',
        ):
            # Without target object, return True with safe methods
            return True

        # === ADMIN RULES ===
        if user.is_superuser:
            # Admin can do everything
            return True

        # === STAFF/USER RULES ===
        return method in ('GET')
