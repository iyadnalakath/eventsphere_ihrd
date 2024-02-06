from django.db import models
from main.models import BaseModel
from projectaccount.models import Account
from django.db.models import Avg
from decimal import Decimal
from django.core.validators import RegexValidator


# Create your models here.
class Area(BaseModel):
    area = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.area



class SubCatagory(BaseModel):
    sub_catagory_name = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(upload_to="mediafiles")

    def __str__(self) -> str:
        return self.sub_catagory_name




class ProfilePic(BaseModel):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="profile", null=True, blank=True
    )
    more_photos = models.ImageField(
        upload_to="mediafiles", null=True, blank=True
    )


class TeamProfile(BaseModel):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="team_profilepic", null=True, blank=True
    )
    team_profile = models.ImageField(
        upload_to="mediafiles", null=True, blank=True
    )


class Service(BaseModel):
    service_name = models.TextField(null=True, blank=True)
    sub_catagory = models.ForeignKey(SubCatagory, on_delete=models.CASCADE)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="event_team"
    )
    popularity = models.FloatField(default=0.0)


    profile = models.ForeignKey(
        ProfilePic,
        on_delete=models.CASCADE,
        related_name="profiles",
        null=True,
        blank=True,
    )
    team_profilepic = models.ForeignKey(
        TeamProfile,
        on_delete=models.CASCADE,
        related_name="team_profiles",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.service_name


class Rating(models.Model):
    
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="ratings"
    )
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="customer"
    )


class Notification(BaseModel):
    subject = models.CharField(max_length=255, null=True, blank=True)
    notification = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True, null=True, blank=True)


class Enquiry(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="enquiries"
    )
    name = models.CharField(max_length=255, null=False, blank=False)
    phone = models.IntegerField(
        validators=[
            RegexValidator(r"^\d{10}$", "Phone number must be exactly 10 digits")
        ],
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

   

class Inbox(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="contact_us"
    )
    email = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True, null=True, blank=True)



class Popularity(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="popular"
    )

class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    district = models.CharField(max_length=50)

