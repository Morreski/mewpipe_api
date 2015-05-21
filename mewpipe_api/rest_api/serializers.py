from rest_framework import serializers
from rest_api.models import Video, Tag
from rest_api.shortcuts import HtmlCleanField


class TagSerializer(serializers.ModelSerializer):
  videos = serializers.SlugRelatedField(
      slug_field = 'uid',
      read_only = True,
      many=True,
  )
  name   = HtmlCleanField(max_length=100 )

  class Meta:
    model = Tag
    fields = Tag.serialized


class VideoSerializer(serializers.ModelSerializer):
  title = HtmlCleanField(max_length=40)
  description = HtmlCleanField(required=False)
  tags = TagSerializer(many=True, read_only=True)

  class Meta:
    model = Video
    fields = Video.serialized
    depth = 1