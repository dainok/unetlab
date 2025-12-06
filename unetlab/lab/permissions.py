"""Permissions for Lab app."""

#############################################################################
# Lab
#############################################################################


class LabPermissionPolicy:
    """Access policy for the Lab model."""

    def can(self, user, method, target, payload):
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

        # === STAFF/USER RULES ===
        user_group_ids = list(user.groups.all().values_list("id", flat=True))
        if target and target.id == user.id:
            # Non-admin users can do anything on their own lab
            return True

        if not target and method == "POST":
            requested_group = payload.get("shared_group")
            if requested_group and requested_group in user_group_ids:
                # Non-admin users can only use the Group objects they belong to
                return True
            elif not requested_group:
                # Non-admin users can create private labs
                return True
            return False

        # Standard users can only read other labs
        return method in ("GET")
