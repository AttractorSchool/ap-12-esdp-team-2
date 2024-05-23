from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return True


class ClubPermission(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if view.action in ['destroy', 'update', 'partial_update']:
            return request.user in obj.managers.all()
        return True


class ClubObjectsPermission(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if view.action in ['destroy', 'update', 'partial_update']:
            return request.user in obj.club.managers.all()
        return True
