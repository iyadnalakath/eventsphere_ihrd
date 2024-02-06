from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import (
    LoginSerializer,
    RegisterCustomerSerializer,
    RegisterEventTeamSerializer,
    UserListSerializer,
    EventManagementListSerializer,
)
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.core.exceptions import PermissionDenied
from rest_framework import generics
from .models import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from django.contrib.auth.views import LoginView
from rest_framework import views
from django.contrib.auth import logout
from django.http import Http404




class RegisterCustomerView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        customer = self.get_object(pk)
        serializer = UserListSerializer(customer)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegisterCustomerSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()

            data["email"] = account.email
            data["username"] = account.username
            data["pk"] = account.pk
            data["response"] = "successfully registered new user."

            token = Token.objects.get(user=account).key
            data["token"] = token

            status_code = status.HTTP_200_OK
            return Response(data, status=status_code)
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class RegisterEventTeamView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterEventTeamSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()

            data["email"] = account.email
            data["username"] = account.username
            data["pk"] = account.pk
            data["response"] = "successfully registered new user."

            token = Token.objects.get(user=account).key
            data["token"] = token

            status_code = status.HTTP_200_OK
            return Response(data, status=status_code)
        else:
            # data = serializer.errors
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by("auto_id")
        if self.request.user.role == "admin":
            serializer = RegisterEventTeamSerializer(queryset, many=True)
            # return super().list(request, *args, **kwargs)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            raise PermissionDenied("You are not allowed to retrieve this object.")


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        context = {}
        if serializer.is_valid():
            user = serializer.validated_data

            username = request.data.get("username")
            password = request.data.get("password")
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)

            context["response"] = "Successfully authenticated."
            context["pk"] = user.pk
            context["username"] = username.lower()
            context["team_name"] = user.team_name
            context["token"] = token.key
            context["role"] = user.role
            context["response"] = "Successfully authenticated."
            return Response(context, status=status.HTTP_200_OK)
        else:
            context["response"] = "Error"
            context["error_message"] = "The username or password is incorrect"
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response(status=204)



class ListUsersView(generics.ListAPIView):
    queryset = Account.objects.filter(role="customer")
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if self.request.user.role == "admin":
            serializer = UserListSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            raise PermissionDenied("You are not allowed to retrieve this object.")

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.role == "admin":
            instance = self.get_object()
            serializer = UserListSerializer(instance)
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to retrieve this object.")
        

class SingleUserView(ModelViewSet):

    queryset = Account.objects.filter(role="customer")
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.role == "admin":
            instance = self.get_object()
            serializer = UserListSerializer(instance)
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to retrieve this object.")
        

    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()
        if request.user.role == "admin":
            profile.delete()
            return Response({"message": "successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        elif request.user.role == "event_management":
            if profile.account.id == self.request.user.id:
                profile.delete()
                return Response({"message": "Profile successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        else:
            raise PermissionDenied("You are not allowed to delete this object.")



class EventManagementUsersView(ModelViewSet):
    queryset = Account.objects.filter(role="event_management")
    serializer_class = EventManagementListSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if self.request.user.role == "admin":
            serializer = EventManagementListSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            raise PermissionDenied("You are not allowed to retrieve this object.")

    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()
        if request.user.role == "admin":
            profile.delete()
            return Response({"message": "successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        elif request.user.role == "event_management":
            if profile.account.id == self.request.user.id:
                profile.delete()
                return Response({"message": "Profile successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        else:
            raise PermissionDenied("You are not allowed to delete this object.")