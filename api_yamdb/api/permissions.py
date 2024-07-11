from rest_framework import permissions


class IsAdminOrReadPermission(permissions.BasePermission):
    """Проверяет является ли пользователь admin."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))
        )


class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser
        )


class IsAuthorOrModeratorOrAdminPermission(permissions.BasePermission):
    """
    Проверяет является ли пользователь author или moderator или admin.
    В противном случае разрешает только безопасные запросы.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
