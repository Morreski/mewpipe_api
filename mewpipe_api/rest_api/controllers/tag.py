from rest_framework import generics
from rest_framework import filters

from rest_api.models import Tag
from rest_api.serializers import TagSerializer

class TagGeneral( generics.ListAPIView):

  queryset = Tag.objects.all()
  serializer_class = TagSerializer
  filter_backends = (filters.OrderingFilter, )
  filter_fields = ('name')
  ordering_fields = filter_fields


class TagSpecific(generics.RetrieveAPIView):

  queryset = Tag.objects.all()
  serializer_class = TagSerializer
  lookup_field = 'uid'
