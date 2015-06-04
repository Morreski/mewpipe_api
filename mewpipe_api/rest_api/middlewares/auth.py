from django.conf import settings
from rest_api.shortcuts import JsonResponse
from rest_api.serializers import UserDetailsSerializer
from rest_api.models import UserAccount
import jwt, time

class JwtAuth(object):

  def process_request(self, request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
      request.user_uid =  None
      return

    try:
      token_data = jwt.decode(token, settings.TOKEN_SECRET)
    except jwt.DecodeError:
      return JsonResponse({"tokenError" : "Token signature verification failed"}, status=400)
    except jwt.ExpiredSignatureError:
      return JsonResponse({"tokenError" : "Token expired"}, status=401)

    request.user_uid = token_data["user"]["uid"]
    return

  def process_response(self, request, response):
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
    print token
    response['HTTP_AUTHORIZATION'] = token
    return response


