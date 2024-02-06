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
    

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(style={"input_type": "password"})

#     def validate(self, data):
#         user = authenticate(**data)
#         if user and user.is_active:
#             return user
#         raise serializers.ValidationError("Incorrect Credentials")
    

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(label=("Username"), write_only=True)
#     password = serializers.CharField(label=("Password"), write_only=True)

#     def create(self, validated_data):
#         context = {}
#         username = validated_data.get("username")
        
#         password = validated_data.get("password")
#         account = authenticate(username=username, password=password)
#         account.save()

#         if account is not None:
#             token, created = Token.objects.get_or_create(user=account)
#             # account.save()
#             context["response"] = "Successfully authenticated."
#             # context["pk"] = user.pk
#             context["username"] = username.lower()
#             context["token"] = token.key
#             # context["role"] = user.role
#             context["response"] = "Successfully authenticated."
#             return Response(context, status=status.HTTP_200_OK)
            
             
#         else:
#             raise serializers.ValidationError(
#                 {"error_message": "The username or password is incorrect"}
#             )

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    pass




class RegisterCustomerSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type': 'password'}, read_only=False)
    # password = serializers.CharField(
    #     write_only = True,
    #     required = True,
    #     help_text = 'Enter password',
    #     style = {'input_type': 'password'}
    # )

    # confirm password field
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Enter confirm password",
        style={"input_type": "password"},
    )

    # role= serializers.CharField(read_only=True)
    class Meta:
        model = Account
        fields = ["full_name", "username", "email", "phone", "password", "password2"]

        read_only_fields = ("password2",)

        extra_kwargs = {
            "password": {"write_only": True},
            # 'password2':{'write_only':True}
        }

        # def save(self):

        #     user = User(
        #         email=self.validated_data['email'],
        #         username=self.validated_data['username'],
        #         phone=self.validated_data['phone'],
        #         full_name=self.validated_data['full_name'],
        #         # password2=self.validated_data('password2')
        #         # role = self.validated_data['role']

        #     )
        #     password = self.validated_data['password']

        #     # password2 =self.validated_data.pop('password2')
        #     password2 = self.validated_data['password2']
        #     if password != password2:
        #         raise serializers.ValidationError({'password': 'Passwords must match.'})
        #     user.set_password(password)
        #     user.save()
        #     return user

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
                # custom_field=validated_data['custom_field']
            )
            # user.save()

            # password = self.validated_data['password']

            #     # password2 =self.validated_data.pop('password2')
            # password2 = self.validated_data['password2']
            # if password != password2:
            #     raise serializers.ValidationError({'password': 'Passwords must match.'})
            user.set_password(validated_data["password"])
            user.role = "customer"
            user.save()
            return user

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.role = 'customer'
    #     if commit:
    #         user.save()
    #     return user

    # def save(self, validated_data):
    #     user=super().save(validated_data)
    #     user.role = 'customer'


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
            #    'profile_pic',
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
    # profile = serializers.SerializerMethodField()
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
            # 'profile_pic'
            "profile"
        )
        
  
    def get_profile(self, obj):
        team_profile = TeamProfile.objects.filter(account=obj).first()
        if team_profile:
            url = team_profile.team_profile.url
            if settings.MEDIA_URL in url:
                return urljoin(settings.HOSTNAME, url)
        return None





#   def get_profile(self, obj):
#         request = self.context.get("request")
#         team_profile = TeamProfile.objects.filter(account=obj).first()
#         if team_profile and team_profile.team_profile:
#             url = team_profile.team_profile.url
#             if request:
#                 return request.build_absolute_uri(url)
#             else:
#                 return url
#         return None