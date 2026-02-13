from rest_framework.permissions import BasePermission
from rest_framework import permissions

# class IsAuthor(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user==obj.owner

# class IsAccountOwner(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user==obj

class IsSuperAdmin(permissions.BasePermission):
    """
    Разрешает доступ только суперадминам (суперпользователям)
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser


class IsAdmin(permissions.BasePermission):
    """
    Разрешает доступ только админам (staff) и суперадминам
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )


class IsIntern(permissions.BasePermission):
    """
    Разрешает доступ обычным пользователям (стажерам), админам и суперадминам
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
