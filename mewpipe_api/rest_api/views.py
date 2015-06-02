from django.contrib.auth import login, logout
from django.shortcuts import render
from django.conf import settings
from django.http import HttpRequest
from .serializers import UserDetailsSerializer

from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.account.views import SignupView, ConfirmEmailView
from allauth.account.utils import complete_signup
from allauth.account import app_settings

from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.serializers import LoginSerializer, TokenSerializer
from rest_auth.views import Login

class SocialLogin(Login):
    serializer_class = SocialLoginSerializer

class FacebookLogin(SocialLogin):
    adapter_class = FacebookOAuth2Adapter

class Register(APIView, SignupView):

    permission_classes = (AllowAny,)
    user_serializer_class = UserDetailsSerializer
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def form_valid(self, form):
        self.user = form.save(self.request)
        if isinstance(self.request, HttpRequest):
            request = self.request
        else:
            request = self.request._request
        return complete_signup(request, self.user,
                               app_settings.EMAIL_VERIFICATION,
                               self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.initial = {}
        self.request.POST = self.request.DATA.copy()
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        if self.form.is_valid():
            self.form_valid(self.form)
            return self.get_response()
        else:
            return self.get_response_with_errors()

    def get_response(self):
        serializer = self.user_serializer_class(instance=self.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_response_with_errors(self):
        return Response(self.form.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(APIView, ConfirmEmailView):

    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        self.kwargs['key'] = self.request.DATA.get('key', '')
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)

class Login(GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = Token
    response_serializer = TokenSerializer

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token, created = self.token_model.objects.get_or_create(
            user=self.user)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            login(self.request, self.user)

    def get_response(self):
        return Response(
            self.response_serializer(self.token).data, status=status.HTTP_200_OK
        )

    def get_error_response(self):
        return Response(
            self.serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=self.request.DATA)
        if not self.serializer.is_valid():
            return self.get_error_response()
        self.login()
        return self.get_response()