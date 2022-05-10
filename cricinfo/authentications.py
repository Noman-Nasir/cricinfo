"""This module adds custom permission classes for API access."""
from rest_framework import permissions


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""

    def has_permission(self, request, view):
        # SAFE_METHODS => GET, HEAD or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser


class IsVerifiedUser(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""

    def has_permission(self, request, view):
        return request.user.is_staff
