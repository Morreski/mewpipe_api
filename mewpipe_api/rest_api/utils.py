from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token

def get_user_by_token(token):
  try:
    token = Token.objects.get(key=token)
  except ObjectDoesNotExist:
    return None

  try:
    user = token.user
  except:
    return None

  return user