from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Admin users can do anything.
    Authenticated users can only read.
    """

    def has_permission(self, request, view):
        # Read-only access for authenticated users
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        # Write permissions only for admin users
        return request.user.is_staff
