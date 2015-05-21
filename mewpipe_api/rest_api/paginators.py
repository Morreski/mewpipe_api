from rest_framework.pagination import LimitOffsetPagination
from django.conf import settings

class BasePaginator(LimitOffsetPagination):
  max_limit = settings.PAGINATION_LIMIT
  default_limit = max_limit

class VideoPaginator(BasePaginator):
  max_limit = settings.VIDEO_PAGINATION_LIMIT
  default_limit = max_limit
