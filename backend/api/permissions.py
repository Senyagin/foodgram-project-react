from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешение прав доступа для автора или только чтение."""
    def has_permission(self, request, view):
        """Предоставляет разрешение аутентифицированному пользователю"""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Предоставляет разрешение автору объекта"""
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return True
        if (request.method in ['DELETE', 'PATCH']
           and request.user == obj.author):
            return True
        return False
