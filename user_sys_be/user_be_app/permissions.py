from rest_framework.permissions import BasePermission

class IsSuperAdminRole:
    def has_permission(self, request):
        payload = getattr(request,"jwt_payload", None)
        if not payload:
            return False
        roles = payload.get("role",[])
        return "superadmin" in roles


class IsUserRole:
    def has_permission(self, request):
        payload = getattr(request,"jwt_payload", None)
        if not payload:
            return False
        roles = payload.get("role",[])
        return "user" in roles