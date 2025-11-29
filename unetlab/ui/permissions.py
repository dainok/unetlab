"""
Permissions for UI app.

Return values of the can method:
- None -> authentication is required.
- True -> action is permitted.
- False -> action is denied.
"""

#############################################################################
# Constance
#############################################################################


class ConstancePermissionPolicy:
    """Access policy for the Constance model."""

    def can(self, user, method):
        """Defines what the requesting user can do based on role and HTTP method."""

        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest access is denied
            return None

        # === ADMIN RULES ===
        if user.is_superuser:
            return True

        # === STAFF/USER RULES ===
        return False


#############################################################################
# Group
#############################################################################


class GroupPermissionPolicy:
    """Access policy for the Group model."""

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
            return True

        # === STAFF/USER RULES ===
        # With target and GET -> Permission granted
        return method in ("GET")


#############################################################################
# User
#############################################################################


class UserPermissionPolicy:
    """Access policy for the User model."""

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
            # Admin can do everything except delete themselves
            if target and target.id == user.id and method == "DELETE":
                return False
            return True

        if method == "POST" and not user.is_superuser:
            # Only admins can create new users
            return False

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


#############################################################################
# Token
#############################################################################


class TokenPermissionPolicy:
    """UI and DRF (API) permisson policy for Token objects."""

    def can(self, user, method, target=None):
        """Defines what the requesting user can do based on target, role and HTTP method."""

        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest access is denied
            return None

        # === COMMON RULES ===
        if target and target.user.id == user.id:
            # Anyone can do anything on owned Tokens
            return True
        if not target and method in (
            "DELETE",
            "GET",
            "HEAD",
            "OPTIONS",
            "PATCH",
            "POST",
            "PUT",
        ):
            # Safe methods are granted to anyone
            return True

        # === ADMIN RULES ===
        if user.is_superuser and method in ("DELETE", "GET"):
            # Admin can always read and delete
            return True

        return False


#############################################################################
# Home
#############################################################################


class HomePermissionPolicy:
    """UI permisson policy for Home."""

    def can(self, user, method):
        """Defines what the requesting user can do based on target, role and HTTP method."""

        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest access is denied
            return None

        # === COMMON RULES ===
        return True
