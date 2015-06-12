from django.views.generic.edit import FormView
from django.contrib.auth import logout
from django.conf import settings
from .serializers import UserDetailsSerializer, LoginSerializer

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_api.forms import UserAccountCreationForm, UpdateProfileForm
from rest_api.shortcuts import JsonResponse, login_required
from rest_api.models import UserAccount, Video, Mail

from open_facebook.api import FacebookAuthorization, OpenFacebook
from open_facebook.exceptions import ParameterException, OAuthException
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

    usr = self.get_user(s.data['identifier'])
    if usr is None:
      return JsonResponse({"error":"User does not exist"}, status=status.HTTP_401_UNAUTHORIZED)

    if not usr.check_password(s.data["password"]):
      return JsonResponse({"error":"Wrong password"}, status=status.HTTP_401_UNAUTHORIZED)

    serialized_user = UserDetailsSerializer(usr)

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

class UserController(APIView, FormView):

  serializer_class = UserDetailsSerializer
  allowed_methods = ('POST', 'PUT', 'OPTIONS', 'HEAD')

  def form_valid(self, form):
    self.user = form.save(self.request)

  def post(self, request, *args, **kwargs):
    self.initial = {}
    self.request.POST = self.request.DATA.copy()
    form_class = UserAccountCreationForm
    self.form = self.get_form(form_class)
    if self.form.is_valid():
      self.user = self.form.save(self.request)

      serialized_user = self.serializer_class(instance=self.user)

      secret = settings.TOKEN_SECRET
      token_payload = {"user" : serialized_user.data, "exp"  : int(time.time()) + settings.TOKEN_TTL}
      token = jwt.encode(
        token_payload,
        secret,
        algorithm="HS256"
      )

      return Response({"token" : token}, status=status.HTTP_201_CREATED)
    else:
      return Response(self.form.errors, status=status.HTTP_400_BAD_REQUEST)

  @login_required
  def put(self, request, *args, **kwargs):
    if not request.user_uid:
      return JsonResponse({}, status=status.HTTP_401_UNAUTHORIZED)

    try:
      user_account = UserAccount.objects.get(uid=request.user_uid)
    except UserAccount.DoesNotExist:
      return JsonResponse({"error":"Wrong User"}, status=status.HTTP_401_UNAUTHORIZED)

    self.initial = {}
    self.request.POST = self.request.DATA.copy()
    form = UpdateProfileForm(self.request.POST, instance=user_account)
    if form.is_valid():
      self.user = form.save()

      serialized_user = UserDetailsSerializer(self.user)
      secret = settings.TOKEN_SECRET
      token_payload = {"user" : serialized_user.data, "exp"  : int(time.time()) + settings.TOKEN_TTL}
      token = jwt.encode(
        token_payload,
        secret,
        algorithm="HS256"
      )

      return JsonResponse({"token" : token}, status=status.HTTP_200_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

  @login_required
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
          return JsonResponse({"error":"Unable to delete all the videos"}, status=status.HTTP_400_BAD_REQUEST)

    try:
      user_account.delete()
    except:
      return JsonResponse({"error":"Unable to delete the User"}, status=status.HTTP_400_BAD_REQUEST)

    resp = JsonResponse({"success": "User successfully deleted with all its videos"}, status=status.HTTP_200_OK)
    resp.no_token = True
    return resp

class FacebookLogin(APIView):

  def post(self, request, *args, **kwargs):
    code = request.data["code"]
    redirect = request.data["redirectUri"]
    client_id = request.data["clientId"]
    try:
      res = FacebookAuthorization.convert_code(code=code, redirect_uri=redirect)
    except ParameterException:
      return JsonResponse({"error": "Wrong code"},status=status.HTTP_400_BAD_REQUEST)
    except:
      return JsonResponse({"error": "Something went wrong during the authentication."},status=status.HTTP_400_BAD_REQUEST)

    access_token = res["access_token"]
    expires = res["expires"]

    graph = OpenFacebook(access_token)
    try:
      graph_dict = graph.get('me', fields='id,first_name, last_name, email, name')
      print graph_dict
    except OAuthException:
      return JsonResponse({"error": "Wrong access token"},status=status.HTTP_400_BAD_REQUEST)
    except:
      return JsonResponse({"error": "Something went wrong during the authentication."},status=status.HTTP_400_BAD_REQUEST)

    if UserAccount.user_exists_for_email(graph_dict["email"]):
      user = UserAccount.objects.get(email=graph_dict["email"])
      user.fb_uid = graph_dict["id"]

      serialized_user = UserDetailsSerializer(user)
      secret = settings.TOKEN_SECRET
      token_payload = {"user" : serialized_user.data, "exp"  : int(time.time()) + settings.TOKEN_TTL}
      token = jwt.encode(
        token_payload,
        secret,
        algorithm="HS256"
      )
      return JsonResponse({"token" : token}, status=status.HTTP_200_OK)

    fields = ["id", "first_name", "last_name", "email", "name"]
    for field in fields:
      if field not in graph_dict:
        return JsonResponse({"error": "Cannot get field : " + field},status=status.HTTP_400_BAD_REQUEST)

    password = uuid.uuid4
    try:
      user = UserAccount(username=graph_dict["name"], first_name=graph_dict["first_name"], last_name=graph_dict["last_name"], email=graph_dict["email"], password=password)
      user.fb_uid = graph_dict["id"]
      user.save()
    except:
      return JsonResponse({"error": "Could not create the user"},status=status.HTTP_400_BAD_REQUEST)

    mail = Mail.objects.get(name="newFacebookAccount")
    mail.send("mewpipe@ang.fr", user.email, password=password)

    serialized_user = UserDetailsSerializer(user)
    secret = settings.TOKEN_SECRET
    token_payload = {"user" : serialized_user.data, "exp"  : int(time.time()) + settings.TOKEN_TTL}
    token = jwt.encode(
      token_payload,
      secret,
      algorithm="HS256"
    )

    return JsonResponse({"token" : token}, status=status.HTTP_200_OK)