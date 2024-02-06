from main.functions import password_generater, send_common_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate, logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.viewsets import ModelViewSet

from account.serializers import (
    RegistrationSerializer,
    AccountPropertiesSerializer,
    ChangePasswordSerializer,
)
from account.models import Account
from rest_framework.authtoken.models import Token
from rest_framework.parsers import (
    JSONParser,
    FormParser,
    MultiPartParser,
    FileUploadParser,
)
from rest_framework.decorators import parser_classes


@api_view(
    [
        "POST",
    ]
)
@permission_classes((AllowAny,))
@parser_classes([JSONParser, FormParser, MultiPartParser, FileUploadParser])
def registration_view(request):
    status_code = status.HTTP_400_BAD_REQUEST
    if request.method == "POST":
        data = {}
        print(request.data["email"])
        email = request.data.get("email", "0").lower()
        print(email)
        if validate_email(email) != None:
            data["error_message"] = "That email is already in use."
            data["response"] = "Error"
            return Response(data)

        username = request.data.get("username", "0")
        if validate_username(username) != None:
            data["error_message"] = "That username is already in use."
            data["response"] = "Error"
            return Response(data)
        request_data = request.data.copy()
        request_data["role"] = "use"
        request_data["creator"] = request.user

        serializer = RegistrationSerializer(data=request_data)
        if serializer.is_valid():
            account = serializer.save()
            data["response"] = "successfully registered new user."
            data["email"] = account.email
            data["username"] = account.username
            data["pk"] = account.pk

            token = Token.objects.get(user=account).key
            data["token"] = token
            status_code = status.HTTP_200_OK
        else:
            data = serializer.errors
        return Response(data, status=status_code)


def validate_email(email):
    account = None
    try:
        account = Account.objects.get(email=email)
        print(account)
    except Account.DoesNotExist:
        return None
    if account != None:
        return email


def validate_username(username):
    account = None
    try:
        account = Account.objects.get(username=username)
    except Account.DoesNotExist:
        return None
    if account != None:
        return username


@api_view(
    [
        "GET",
    ]
)
@permission_classes((IsAuthenticated,))
def account_properties_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = AccountPropertiesSerializer(account)
        return Response(serializer.data)


@api_view(
    [
        "POST",
    ]
)
@permission_classes((IsAuthenticated,))
def update_account_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":
        serializer = AccountPropertiesSerializer(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["response"] = "Account update success"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "POST",
    ]
)
@permission_classes((AllowAny,))
@parser_classes([JSONParser, FormParser, MultiPartParser, FileUploadParser])
def login_view(request):
    context = {}
    username = request.data.get("username")
    password = request.data.get("password")
    account = authenticate(username=username, password=password)

    if account:
        try:
            token = Token.objects.get(user=account)
        except Token.DoesNotExist:
            token = Token.objects.create(user=account)
        context["response"] = "Successfully authenticated."
        context["pk"] = account.pk
        context["username"] = username.lower()
        context["token"] = token.key
        context["role"] = account.role
        return Response(context, status=status.HTTP_200_OK)
    else:
        context["response"] = "Error"
        context["error_message"] = "The username or password is incorrect"
        return Response(context, status=status.HTTP_401_UNAUTHORIZED)


@api_view(
    [
        "POST",
    ]
)
@permission_classes((AllowAny,))
@parser_classes([JSONParser, FormParser, MultiPartParser, FileUploadParser])
def logout_view(request):
    context = {}
    try:
        request.user.auth_token.delete()
        # logout(request)
        context["response"] = "LogOut Successful."
        status_code = status.HTTP_200_OK
    except:
        context["response"] = "Error"
        context["error_message"] = "Invalid Token"
        status_code = status.HTTP_400_BAD_REQUEST

    return Response(context, status=status_code)


@api_view(["GET", "POST"])
@permission_classes((IsAuthenticated,))
@parser_classes([JSONParser, FormParser, MultiPartParser, FileUploadParser])
def profile_view(request):
    status_code = status.HTTP_400_BAD_REQUEST
    context = {}
    if Account.objects.filter(pk=request.user.pk).exists():
        user = Account.objects.get(pk=request.user.pk)
        context["username"] = user.username
        context["email"] = user.email
        context["phone"] = user.phone
        context["full_name"] = user.full_name

        status_code = status.HTTP_200_OK
    return Response(context, status=status_code)


@api_view(
    [
        "GET",
    ]
)
@permission_classes([])
@authentication_classes([])
def does_account_exist_view(request):
    if request.method == "GET":
        email = request.GET["email"].lower()
        data = {}
        try:
            account = Account.objects.get(email=email)
            data["response"] = email
        except Account.DoesNotExist:
            data["response"] = "Account does not exist"
        return Response(data)


@permission_classes((AllowAny,))
class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = Account
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # confirm the new passwords match
            new_password = serializer.data.get("new_password")
            confirm_new_password = serializer.data.get("confirm_new_password")
            if new_password != confirm_new_password:
                return Response(
                    {"new_password": ["New passwords must match"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            # print("-----------------",self.object)
            self.object.save()
            return Response(
                {"response": "successfully changed password"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "POST",
    ]
)
@permission_classes((AllowAny,))
def forgot_password(request):
    # Check old password
    data = {}
    if Account.objects.filter(email=request.data.get("email")).exists():
        password = password_generater(8)

        account = Account.objects.get(email=request.data.get("email"))
        account.set_password(password)
        account.save()
        # from_email = "mail.osperb@gmail.com"
        to_email = account.email
        subject = "Password changed Successfully"
        html_context = {
            "title": "Password changed Successfully",
            "data": [
                {"label": "username", "value": account.username},
                {"label": "Your New Password", "value": password},
            ],
        }
        text_content = str(html_context)
        send_common_mail(html_context, to_email, subject)
        data["response"] = "Your new password has been sent to your email"

    else:
        data["response"] = "Email does not exist"

    return Response(data, status=status.HTTP_200_OK)
