from django.core.exceptions import PermissionDenied


class AdminOnlyMixin:
    def check_permissions(self, request):
        if request.user.role != "admin":
            raise PermissionDenied("You are not allowed to perform this action.")
