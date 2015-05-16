from rest_framework import generics

from rest_api.models import Tag
from rest_api.serializers import TagSerializer

class TagGeneral( generics.ListAPIView):

  queryset = Tag.objects.all()
  serializer_class = TagSerializer

class TagSpecific(generics.RetrieveAPIView):

  queryset = Tag.objects.all()
  serializer_class = TagSerializer
  lookup_field = 'uid'
