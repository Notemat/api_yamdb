from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    """Проверяет является ли пользователь admin."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
        )
