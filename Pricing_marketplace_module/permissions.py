# permissions.py

from rest_framework import permissions


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is a seller
        return request.user.is_seller
