"""Permissions for Task app."""

#############################################################################
# Task
#############################################################################


class TaskPermissionPolicy:
    """Access policy for the Task model."""

    def can(self, user, method, target, payload):
        """Defines what the requesting user can do based on target, role and HTTP method."""

        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest access is denied
            return None

        # === COMMON RULES ===
        if not target and method in (
            'DELETE',
            'GET',
            'HEAD',
            'OPTIONS',
            'PATCH',
            'PUT',
        ):
            # Safe methods are granted to anyone
            return True

        # All users can only read other labs
        return method in ('GET')


#############################################################################
# Log
#############################################################################


class LogPermissionPolicy:
    """Access policy for the Task model."""

    def can(self, user, method, target, payload):
        """Defines what the requesting user can do based on target, role and HTTP method."""

        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest access is denied
            return None

        # === COMMON RULES ===
        if not target and method in (
            'DELETE',
            'GET',
            'HEAD',
            'OPTIONS',
            'PATCH',
            'PUT',
        ):
            # Safe methods are granted to anyone
            return True

        # All users can only read other labs
        return method in ('GET')
