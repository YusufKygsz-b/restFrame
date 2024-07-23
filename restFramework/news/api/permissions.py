from rest_framework import permissions
from pprint import pprint

class IsAdminUserorReadOnly(permissions.IsAdminUser):
    def has_permission(self, request ,view):
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin
    

class IsSuperUserOnly(permissions.BasePermission):
    """
    Custom permission to only allow super users to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and is a superuser
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)