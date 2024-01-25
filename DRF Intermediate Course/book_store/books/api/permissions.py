from rest_framework import permissions


class IsAdminStaffOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or \
            request.user.is_superuser or request.user.is_staff


class IsCommentOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or \
            request.user == obj.commentor
