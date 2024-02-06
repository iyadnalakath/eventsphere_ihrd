from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = (
        "pk",
        "username",
        "phone",
        "date_joined",
        "last_login",
        "email",
        "is_admin",
        "is_active",
        "full_name",
        "role",
        "team_name",
        "work_time",
        "over_view",
        "address",
        "pin_code",
        "district",
    )
    search_fields = (
        "pk",
        "phone",
    )
    readonly_fields = ("pk", "date_joined", "last_login")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)


