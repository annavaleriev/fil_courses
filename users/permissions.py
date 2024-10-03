from rest_framework import permissions

from users.models import MODER_GROUP_NAME


class NotIsModer(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name=MODER_GROUP_NAME).exists()


class IsOwnerSuperUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user == obj.owner
