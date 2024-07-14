from rest_framework import permissions


class IsAdminOrReadPermission(permissions.BasePermission):
    """Разрешены безопасные запросы и от admin."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))
        )


class IsAdminPermission(permissions.BasePermission):
    """Доступ только для admin и superuser."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class IsAuthorOrModeratorOrAdminPermission(permissions.BasePermission):
    """Разрешены безопасные запросы и от admin/moderator/author."""

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
