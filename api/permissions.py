from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser

""" Define custom permissions"""

class IsAdminOrReadOnly(permissions.BasePermission):
    """Allows non_safe methods only to Admin"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.is_superuser


class IsAdminReadOnly(permissions.BasePermission):
    """Allow only the Admin to make a get Request to all Users Data"""

    def has_permission(self, request, view):
        if request.method != "GET":
            return True
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.is_superuser
