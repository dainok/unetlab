from rest_framework.permissions import BasePermission
from unetlab import messages

class IsAdminOrStaff(BasePermission):
    """
    Allows access only to admin or staff users.
    """
    message = messages.PERMISSION_ADMIN

    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_superuser)
