from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Is author or read only permission."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """Is admin or read only permission."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
        )
