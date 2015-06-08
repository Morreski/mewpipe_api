from django.views.generic.edit import FormView
from django.contrib.auth import logout
from django.http import HttpRequest
from django.conf import settings
from .serializers import UserDetailsSerializer, PasswordChangeSerializer, LoginSerializer

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

from rest_api.forms import UserAccountCreationForm
from rest_api.shortcuts import JsonResponse
from rest_api.models import UserAccount, Video
from rest_auth.registration.serializers import SocialLoginSerializer
import jwt, time


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
      return JsonResponse(s.errors, status=status.HTTP_400_BAD_REQUEST)

    u = self.get_user(s.data['identifier'])
    if u is None:
      return JsonResponse({"error":"User does not exist"}, status=status.HTTP_401_UNAUTHORIZED)

    if not u.check_password(s.data["password"]):
      return JsonResponse({{"error":"Wrong password"}}, status=status.HTTP_401_UNAUTHORIZED)

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

  def post(self, request):
    logout(request)
    return Response({"success": "Successfully logged out."},status=status.HTTP_200_OK)

class SocialLogin(Login):
  serializer_class = SocialLoginSerializer

class FacebookLogin(SocialLogin):
  adapter_class = FacebookOAuth2Adapter

class UserController(APIView, FormView):

  serializer_class = UserDetailsSerializer
  allowed_methods = ('POST', 'PUT', 'OPTIONS', 'HEAD')

  def form_valid(self, form):
    self.user = form.save(self.request)

  def get_response(self):
    serializer = self.serializer_class(instance=self.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def post(self, request, *args, **kwargs):
    self.initial = {}
    self.request.POST = self.request.DATA.copy()
    form_class = UserAccountCreationForm
    self.form = self.get_form(form_class)
    if self.form.is_valid():
      self.user = self.form.save(self.request)
      return self.get_response()
    else:
      return Response(self.form.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, *args, **kwargs):
    if not request.user_uid:
      return JsonResponse({}, status=status.HTTP_401_UNAUTHORIZED)

    try:
      user_account = UserAccount.objects.get(uid=request.user_uid)
    except UserAccount.DoesNotExist:
      return JsonResponse({"error":"Wrong User"}, status=status.HTTP_401_UNAUTHORIZED)
    serialized_user = UserDetailsSerializer(user, data=request.data)
    if serialized_user.is_valid():
      serialized_user.save()

      secret = settings.TOKEN_SECRET
      token_payload = {"user" : serialized_user.data, "exp"  : int(time.time()) + settings.TOKEN_TTL}
      token = jwt.encode(
        token_payload,
        secret,
        algorithm="HS256"
      )

      return JsonResponse({"token" : token, "user" : serialized_user.data},)
    return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, *args, **kwargs):
    if not request.user_uid:
      return JsonResponse({"error":"Not authentified"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
      user_account = UserAccount.objects.get(uid=request.user_uid)
    except UserAccount.DoesNotExist:
      return JsonResponse({"error":"Wrong User"}, status=status.HTTP_401_UNAUTHORIZED)

    videos = Video.objects.filter(author=user_account)

    if len(videos) != 0:
      for vid in videos:
        try:
          vid.delete()
        except:
          return Response({"error":"Unable to delete all the videos"}, status=status.HTTP_400_BAD_REQUEST)

    try:
      user_account.delete()
    except:
      return Response({"error":"Unable to delete the User"}, status=status.HTTP_400_BAD_REQUEST)

    resp = Response({"success": "User successfully deleted with all its videos"}, status=status.HTTP_200_OK)
    resp.no_token = True
    return resp

class PasswordChange(GenericAPIView):

  serializer_class = PasswordChangeSerializer

  def post(self, request):
    serializer = self.get_serializer(data=request.DATA)
    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response({"success": "New password has been saved."})
