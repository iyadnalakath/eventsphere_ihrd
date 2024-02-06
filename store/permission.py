from rest_framework import permissions
from rest_framework.permissions import IsAdminUser

from rest_framework import status

# class AdminCustomerEventTeam(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user.role=='admin':
#             if request.method == ['GET','POST','PUT','PATCH']:
#                 return True
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         elif request.user.role=='customer':
#             if request.method ==['GET']:
#                 return True
#             return Response(status=status.HTTP_400_BAD_REQUEST)
from rest_framework.response import (
    Response,
)  #         elif request.user.event_management==['GET','POST','PUT','PATCH']:

#             return True


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"
