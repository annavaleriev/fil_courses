from rest_framework import permissions


class IsModer(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsSuperUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
