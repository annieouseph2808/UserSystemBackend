from rest_framework.permissions import BasePermission

class IsSuperAdminRole(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name="superadmin").exists()
        )


class IsUserRole(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name="user").exists()
        )