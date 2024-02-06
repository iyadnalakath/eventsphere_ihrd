from django.db import models
from rest_framework import serializers

from account.models import Account
from main.functions import  password_generater, send_common_mail






class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email','username','phone','password', 'password2','full_name','role']
        extra_kwargs = {
                'password': {'write_only': True},
        }    


    def save(self):

        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            phone=self.validated_data['phone'],
            full_name=self.validated_data['full_name'],
            role = self.validated_data['role']
            
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account


class AccountPropertiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['pk', 'email', 'username', ]

class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id','email', 'username', 'phone','full_name','role']


