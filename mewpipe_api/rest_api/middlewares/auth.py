from django.conf import settings
from rest_api.shortcuts import JsonResponse
from rest_api.serializers import UserDetailsSerializer
from rest_api.models import UserAccount
import jwt, time

class JwtAuth(object):

  def process_request(self, request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    auth_token = auth_header if auth_header is not None else request.GET.get('token')
    if not auth_token:
      request.user_uid = None
      return

    token_args = auth_token.split(' ')
    if len(token_args) < 2:
      token = token_args[0]
    else:
      token = token_args[1]

    try:
      token_data = jwt.decode(token, settings.TOKEN_SECRET)
    except jwt.DecodeError:
      return JsonResponse({"tokenError" : "Token signature verification failed"}, status=400)
    except jwt.ExpiredSignatureError:
      return JsonResponse({"tokenError" : "Token expired"}, status=401)

    request.user_uid = token_data["user"]["uid"]
    return

  def process_response(self, request, response):
    if hasattr(response, "no_token"):
      if response.no_token:
        return response

    if response.status_code != 200:
      return response

    if not request.user_uid:
      return response

    user = UserAccount.objects.get(uid=request.user_uid)
    serialized_user = UserDetailsSerializer(user)
    token_payload = {"user" : serialized_user.data, "exp"  : int(time.time()) + settings.TOKEN_TTL}
    token = jwt.encode(
      token_payload,
      settings.TOKEN_SECRET,
      algorithm="HS256"
    )
    response['Authorization'] = token
    return response
