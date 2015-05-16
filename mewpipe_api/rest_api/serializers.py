from rest_framework import serializers
from rest_api.models import Video, Tag
from rest_api.shortcuts import HtmlCleanField

class VideoSerializer(serializers.ModelSerializer):
  title = HtmlCleanField(max_length=40)
  description = HtmlCleanField(required=False)

  class Meta:
    model = Video
    fields = Video.serialized
    depth = 1

class TagSerializer(serializers.ModelSerializer):
  name = HtmlCleanField(max_length=100 )

  class Meta:
    model = Tag
