"""Permissions for Lab app."""

#############################################################################
# Lab
#############################################################################


class LabPermissionPolicy:
    """Access policy for the Lab model."""

    def can(self, user, method, target=None):
        """Defines what the requesting user can do based on target, role and HTTP method."""

        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest access is denied
            return None

        # === COMMON RULES ===
        if not target and method in (
            "DELETE",
            "GET",
            "HEAD",
            "OPTIONS",
            "PATCH",
            "PUT",
        ):
            # Safe methods are granted to anyone
            return True

        # === ADMIN RULES ===
        if user.is_superuser:
            # Admin can do everything
            return True

        # === STAFF RULES ===
        if user.is_staff:
            if target:
                if target.id == user.id:
                    # Staff users can do anything on their own profile
                    return True
                if target.is_superuser or target.is_staff:
                    # Staff users cannot modify/delete other staffs/admins
                    return method in ("GET", "HEAD", "OPTIONS")
            return True

        # === STANDARD USER RULES ===
        if target and target.id == user.id:
            # Standard users can do anything on their own profile
            return True

        # Standard users can only read other staffs/admins/users
        return method in ("GET")
