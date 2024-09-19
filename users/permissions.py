from rest_framework import permissions

from users.models import MODER_GROUP_NAME


class IsModer(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name=MODER_GROUP_NAME).exists()


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsSuperUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
