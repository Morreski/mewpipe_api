from django.shortcuts import render
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLogin
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from allauth.account.views import SignupView, ConfirmEmailView
from allauth.account.utils import complete_signup
from allauth.account import app_settings

from .serializers import UserDetailsSerializer
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.views import Login

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