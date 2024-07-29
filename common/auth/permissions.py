from rest_framework.permissions import BasePermission


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.is_admin:
            return True

        return False
