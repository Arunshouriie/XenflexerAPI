# accounts/permissions.py
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Object-level permission to only allow users to access or modify their own data.
    Assumes the model instance has a `user` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Only allow access if the object's user matches the authenticated user
        return obj.user == request.user
