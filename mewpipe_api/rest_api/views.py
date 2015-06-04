from django.contrib.auth import logout
from django.http import HttpRequest
from django.conf import settings
from .serializers import UserDetailsSerializer, PasswordChangeSerializer, LoginSerializer
from .permissions import IsAnonymous

from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.account.views import SignupView, ConfirmEmailView
from allauth.account.utils import complete_signup
from allauth.account import app_settings

from rest_api.shortcuts import JsonResponse
from rest_api.models import UserAccount
from rest_auth.registration.serializers import SocialLoginSerializer
import jwt, time
"""
class Login(GenericAPIView):

  permission_classes = (IsAnonymous,)
  serializer_class = LoginSerializer
  token_model = Token
  response_serializer = TokenSerializer

  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return super(Login, self).dispatch(request, *args, **kwargs)

  def login(self):
      self.user = self.serializer.validated_data['user']
      self.token, created = self.token_model.objects.get_or_create(user=self.user)
      if getattr(settings, 'REST_SESSION_LOGIN', True):
        login(self.request, self.user)

  def get_error_response(self):
    return Response(
      self.serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )

  def post(self, request, *args, **kwargs):
    self.serializer = self.get_serializer(data=self.request.DATA)
    if not self.serializer.is_valid():
      return self.get_error_response()
    self.login()
    return Response({'token': self.token.key}, status=status.HTTP_200_OK)
"""
class Login(APIView):

  def get_user(self, identifier):
    try:
      return UserAccount.objects.get(username=identifier)
    except UserAccount.DoesNotExist:
      pass

    try:
      return UserAccount.objects.get(email=identifier)
    except UserAccount.DoesNotExist:
      pass

    return None

  def post(self, request, *args, **kwargs):
    s = LoginSerializer(data=request.data)
    if not s.is_valid():
      return JsonResponse(s.errors, status=400)

    u = self.get_user(s.data['identifier'])
    if u is None:
      return JsonResponse({}, status=404)

    if not u.check_password(s.data["password"]):
      return JsonResponse({}, status=401)

    serialized_user = UserDetailsSerializer(u)

    #Let the magic do the work !
    secret = settings.TOKEN_SECRET
    token_payload = {"user" : serialized_user.data, "exp"  : int(time.time()) + settings.TOKEN_TTL}
    token = jwt.encode(
        token_payload,
        secret,
        algorithm="HS256"
    )

    return JsonResponse(
        {"token" : token},
    )

class Logout(APIView):

  permission_classes = (IsAuthenticated,)

  def post(self, request):
    try:
      request.user.auth_token.delete()
    except:
      pass

    logout(request)
    return Response({"success": "Successfully logged out."},status=status.HTTP_200_OK)

class SocialLogin(Login):
  serializer_class = SocialLoginSerializer

class FacebookLogin(SocialLogin):
  adapter_class = FacebookOAuth2Adapter

class Register(APIView, SignupView):

  permission_classes = (IsAnonymous,)
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
    return complete_signup(request, self.user, app_settings.EMAIL_VERIFICATION, self.get_success_url())

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


class UserDetails(RetrieveUpdateAPIView):

  authentication_classes = (TokenAuthentication,)
  serializer_class = UserDetailsSerializer
  permission_classes = (IsAuthenticated,)

  def get_object(self):
    return self.request.user

class PasswordChange(GenericAPIView):

  serializer_class = PasswordChangeSerializer
  permission_classes = (IsAuthenticated,)
  authentication_classes = (TokenAuthentication,)

  def post(self, request):
    serializer = self.get_serializer(data=request.DATA)
    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response({"success": "New password has been saved."})
