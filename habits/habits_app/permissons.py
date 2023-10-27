from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Проверка прав доступа по факту владения привычкой"""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator
