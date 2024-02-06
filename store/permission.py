from rest_framework import permissions
from rest_framework.permissions import IsAdminUser

from rest_framework import status


from rest_framework.response import (
    Response,
)  

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"
