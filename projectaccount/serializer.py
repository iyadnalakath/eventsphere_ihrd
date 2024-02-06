from rest_framework import serializers
from store.models import TeamProfile
from django.contrib.auth import authenticate
from .models import Account
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from urllib.parse import urljoin



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class LogoutSerializer(serializers.Serializer):
    pass




class RegisterCustomerSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Enter confirm password",
        style={"input_type": "password"},
    )

    class Meta:
        model = Account
        fields = ["full_name", "username", "email", "phone", "password", "password2"]

        read_only_fields = ("password2",)

        extra_kwargs = {
            "password": {"write_only": True},
          
        }

    def create(self, validated_data):
        password = self.validated_data["password"]

        # password2 =self.validated_data.pop('password2')
        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        else:
            user = Account.objects.create(
                username=validated_data["username"],
                email=validated_data["email"],
                full_name=self.validated_data["full_name"],
                phone=self.validated_data["phone"],
               
            )

            user.set_password(validated_data["password"])
            user.role = "customer"
            user.save()
            return user


class RegisterEventTeamSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Enter confirm password",
        style={"input_type": "password"},
    )

    class Meta:
        model = Account
        fields = [
            "team_name",
            "username",
            "email",
            "phone",
            "place",
            "work_time",
            "over_view",
            "address",
            "password",
            "password2",
            "pin_code",
            "district",
        ]

        read_only_fields = ("password2",)

        extra_kwargs = {
            "password": {"write_only": True},
            # 'password2':{'write_only':True}
        }

    def create(self, validated_data):
        password = self.validated_data["password"]

        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        else:
            user = Account.objects.create(
                username=validated_data["username"],
                email=validated_data["email"],
                team_name=self.validated_data["team_name"],
                phone=self.validated_data["phone"],
                place=self.validated_data["place"],
                work_time=self.validated_data["work_time"],
                over_view=self.validated_data["over_view"],
                address=self.validated_data["address"],
                pin_code=self.validated_data["pin_code"],
                district=self.validated_data["district"],
                # profile_pic=self.validated_data['profile_pic']
                password=self.validated_data["password"],
            )

            user.set_password(validated_data["password"])
            user.role = "event_management"
            user.save()
            return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "id",
            "username",
            "is_staff",
            "last_login",
            "over_view",
            "work_time",
            "is_admin",
            "is_active",
            "full_name",
            "role",
            "email",
            "is_staff",
            "address",
            "phone",
            "dob",
            "work_time",
            "date_joined",
            "place",
        )


class EventManagementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "id",
            "team_name",
            "username",
            "email",
            "phone",
            "place",
            "work_time",
            "over_view",
            "address",
            "profile"
        )
        
  
    def get_profile(self, obj):
        team_profile = TeamProfile.objects.filter(account=obj).first()
        if team_profile:
            url = team_profile.team_profile.url
            if settings.MEDIA_URL in url:
                return urljoin(settings.HOSTNAME, url)
        return None





