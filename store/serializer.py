from rest_framework import serializers
from .models import *
from main.functions import get_auto_id, password_generater
from projectaccount.serializer import RegisterEventTeamSerializer
from projectaccount.models import Account


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ["id", "area"]

        extra_kwargs = {"auto_id": {"read_only": True}}

    def create(self, validated_data):
        area = Area.objects.create(
            **validated_data,
            auto_id=get_auto_id(Area),
           
        )
        return area



class SubCatagorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SubCatagory
        fields = [
            "id",
            "sub_catagory_name",
           
            "image",
        ]

        extra_kwargs = {"auto_id": {"read_only": True}}

    def create(self, validated_data):
        subcatagory = SubCatagory.objects.create(
            **validated_data,
            auto_id=get_auto_id(SubCatagory),
           
        )
        return subcatagory


class EventTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "username",
            "team_name",
            "phone",
            "place",
            "work_time",
            "over_view",
            "address",
            "district",
            "email"
            
        ]

        def create(self, validated_data):
            password = password_generater(8)
            validated_data["password"] = password
            validated_data["password2"] = password

            account_serializer = EventTeamSerializer(data=validated_data)
            if account_serializer.is_valid():
                account = account_serializer.save()

            return account


class ProfileEventTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "username",
            "team_name",
           
        ]

        def create(self, validated_data):
            password = password_generater(8)
            validated_data["password"] = password
            validated_data["password2"] = password

            account_serializer = EventTeamSerializer(data=validated_data)
            if account_serializer.is_valid():
                account = account_serializer.save()

            return account

class ProfileSerializer(serializers.ModelSerializer):
   
    account_view = ProfileEventTeamSerializer(read_only=True, source="account")

    class Meta:
        model = ProfilePic
        fields = ("id", "account", "account_view", "more_photos")
        extra_kwargs = {"auto_id": {"read_only": True}}

    def create(self, validated_data):
        profile_pic = ProfilePic.objects.create(
            **validated_data,
            auto_id=get_auto_id(ProfilePic),
            
        )
        return profile_pic

class TeamProfileSerializer(serializers.ModelSerializer):
    account_view = ProfileEventTeamSerializer(read_only=True, source="account")

    class Meta:
        model = TeamProfile
        fields = ("id", "account", "account_view", "team_profile")
        extra_kwargs = {"auto_id": {"read_only": True}}

    def create(self, validated_data):
        team_profile = TeamProfile.objects.create(
            **validated_data,
            auto_id=get_auto_id(TeamProfile),
           
        )
        return team_profile


class RatingSerializer(serializers.ModelSerializer):

    customer_view = serializers.CharField(source="customer.username", read_only=True)

    class Meta:
        model = Rating
        fields = [
            "id",
            "service",
            "rating",
            "review",
            "created_at",
            "customer",
            "customer_view"
           
        ]
        extra_kwargs = {
            # 'auto_id': {'read_only': True},
            "customer_view ": {"read_only": True}
            # "service": {"read_only": True}
        }

    def validate_rating(self, value):
        if value > 5.0 or value < 0.0:
            raise serializers.ValidationError("Rating should be between 0.0 and 5.0")
        return value


class ServiceSerializer(serializers.ModelSerializer):
    account_view = EventTeamSerializer(read_only=True, source="account")

    profile = serializers.SerializerMethodField()
    team_profilepic = serializers.SerializerMethodField()

    sub_catagory_name = serializers.CharField(
        source="sub_catagory.sub_catagory_name", read_only=True
    )
    avg_ratings = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            "id",
            "service_name",
            "auto_id",
            "sub_catagory",
            "sub_catagory_name",    
            "account",
            "account_view",
            "avg_ratings",
            "profile",
            "team_profilepic"
        ]

        extra_kwargs = {
            "auto_id": {"read_only": True},
            "rating": {"read_only": True},
        }


    def get_profile(self, obj):
        request = self.context.get("request")
        profile_pics = ProfilePic.objects.filter(account=obj.account)
        profiles = [{"id": profile.id, "url": profile.more_photos.url} for profile in profile_pics]
        if request:
            profiles = [{"id": profile["id"], "url": request.build_absolute_uri(profile["url"])} for profile in profiles]
        return profiles


    def get_team_profilepic(self, obj):
        request = self.context.get("request")
        team_profile = TeamProfile.objects.filter(account=obj.account).first()
        if team_profile:
            url = team_profile.team_profile.url
            if request:
                return request.build_absolute_uri(url)
            else:
                return url
        return None
    
    def get_avg_ratings(self, service):
        account_id = service.account_id
        ratings = Rating.objects.filter(service__account_id=account_id)
        if ratings.exists():
            return ratings.aggregate(avg_ratings=Avg('rating'))['avg_ratings']
        else:
            return None


    def create(self, validated_data):
        service = Service.objects.create(
            **validated_data,
            auto_id=get_auto_id(Service),
            
        )
        return service


class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "username",
            "full_name",
            "phone"
           
        ]

        def create(self, validated_data):
            password = password_generater(8)
            validated_data["password"] = password
            validated_data["password2"] = password

            account_serializer = CustomerUserSerializer(data=validated_data)
            if account_serializer.is_valid():
                account = account_serializer.save()

            return account



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "notification", "subject", "date"]
        extra_kwargs = {"auto_id": {"read_only": True}}

    def create(self, validated_data):
        notification = Notification.objects.create(
            **validated_data,
            auto_id=get_auto_id(Notification),
            
        )
        return notification


class EnquirySerializer(serializers.ModelSerializer):

    class Meta:
        model = Enquiry
        fields = ("id", "service", "phone", "created_at", "name")


class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        fields = ("id", "service", "email", "subject", "message", "date")


class PopularitySerializer(serializers.ModelSerializer):
    service = ServiceSerializer(source=Service)
    event_management_name = serializers.CharField(
        source="service.account__team_name", read_only=True
    )
    rating = serializers.FloatField(source="service.ratings__rating")

    class Meta:
        model = Popularity
        fields = ("id", "service", "event_management_name", "rating")


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'latitude', 'longitude', 'district')
        read_only_fields = ('district',)