from django.contrib import admin
from .models import *

# Register your models here.


class AreaAdmin(admin.ModelAdmin):
    list_display = ("id", "area")


admin.site.register(Area, AreaAdmin)


class SubCatagoryAdmin(admin.ModelAdmin):
    list_display = ("id", "sub_catagory_name", "image")


admin.site.register(SubCatagory, SubCatagoryAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "service_name", "sub_catagory","account")


admin.site.register(Service, ServiceAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "rating", "service", "review", "created_at", "customer")


admin.site.register(Rating, RatingAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "notification", "subject", "date")


admin.site.register(Notification, NotificationAdmin)


class ProfilePicAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "more_photos")


admin.site.register(ProfilePic, ProfilePicAdmin)




class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("id", "service", "name", "phone", "created_at")


admin.site.register(Enquiry, EnquiryAdmin)


class InboxAdmin(admin.ModelAdmin):
    list_display = ("id", "service", "email", "subject", "message", "date")


admin.site.register(Inbox, InboxAdmin)

class TeamProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "team_profile")


admin.site.register(TeamProfile, TeamProfileAdmin)