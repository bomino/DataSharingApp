# permissions.py
from rest_framework import permissions

class IsAnalystOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or 
            request.user.role in ['analyst', 'admin']
        )
    


class IsAnalystOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow analysts and admins to access the API.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
            
        # Allow access to admin users
        if request.user.is_superuser:
            return True
            
        # Allow access to analysts
        if request.user.role == 'analyst':
            return True
            
        return False

    def has_object_permission(self, request, view, obj):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
            
        # Allow access to admin users
        if request.user.is_superuser:
            return True
            
        # Allow analysts to access only their own uploaded files
        if request.user.role == 'analyst':
            return obj.uploaded_by == request.user
            
        return False