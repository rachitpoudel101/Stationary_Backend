from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """
    Allows access only to super admin.
    """

    message = "You are not authorized to perform this action."

    def has_permission(self, request, view):
        user = request.user
        # Only allow authenticated superusers or staff
        return bool(user and user.is_authenticated and (user.is_superuser))


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"


class Isstaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "staff"
