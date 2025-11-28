"""Permissions for UI app."""

#############################################################################
# Constance
#############################################################################


class ConstancePermissionPolicy:
    """
    Policy per TemplateView.
    """

    def can(self, user, method):
        """
        Restituisce:
        - True: ha permesso → mostra la view
        - False: utente autenticato ma senza permesso → 403
        - None: utente anonimo → 401 / redirect
        """
        if not user.is_authenticated:
            return None
        if user.is_superuser:
            return True
        return False


#############################################################################
# Group
#############################################################################


class GroupPermissionPolicy:
    """UI and DRF (API) permisson policy for Group objects."""

    def can(self, user, method, target=None):
        """Defines what the requesting user can do based on their role and HTTP method."""

        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest users are not allowed to do anything
            return None

        # === COMMON RULES ===
        if not target and method in (
            "GET",
            "OPTIONS",
            "HEAD",
            "PUT",
            "PATCH",
            "DELETE",
        ):
            # Without target object, return True with safe methods
            return True

        # === ADMIN RULES ===
        if user.is_superuser:
            # Admin can do everything
            return True

        # === STAFF RULES ===
        return method in ("GET")


#############################################################################
# User
#############################################################################


class UserPermissionPolicy:
    """UI and DRF (API) permisson policy for User objects."""

    def can(self, user, method, target=None):
        """Defines what the requesting user can do based on their role and HTTP method."""

        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest users are not allowed to do anything
            return None

        # === COMMON RULES ===
        if not target and method in (
            "GET",
            "OPTIONS",
            "HEAD",
            "PUT",
            "PATCH",
            "DELETE",
        ):
            # Without target object, return True with safe methods
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
        """Defines what the requesting user can do based on their role and HTTP method."""

        # === GUEST RULES ===
        if not user.is_authenticated:
            # Guest users are not allowed to do anything
            return None

        # === COMMON RULES ===
        if target and target.user.id == user.id:
            # Anyone can do anything on owned Tokens
            return True

        # Without target object, any method is safe
        return True


#############################################################################
# Home
#############################################################################


class HomePermissionPolicy:
    """
    Policy per TemplateView.
    """

    def can(self, user, method):
        """
        Restituisce:
        - True: ha permesso → mostra la view
        - False: utente autenticato ma senza permesso → 403
        - None: utente anonimo → 401 / redirect
        """
        if not user.is_authenticated:
            return None
        return True
