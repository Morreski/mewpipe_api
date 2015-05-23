from rest_framework import serializers
from rest_api.models import Video, Tag
from rest_api.shortcuts import HtmlCleanField


class UserAccountSerializer(serializers.ModelSerializer):
  first_name  = serializers.CharField()
  last_name   = serializers.CharField()
  email       = serializers.CharField()
  username    = serializers.CharField()
  birth_date  = serializers.DateTimeField()
  is_active   = serializers.BooleanField(read_only=True)

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

class ShareSerializer(serializers.Serializer):
  sender_address = serializers.EmailField()
  dest_addresses = serializers.ListField(child=serializers.EmailField())
  video_link     = HtmlCleanField()

class UploadSerializer(serializers.Serializer):
  file = serializers.FileField(use_url=False)

class VideoSerializer(serializers.ModelSerializer):
  title = HtmlCleanField(max_length=40)
  description = HtmlCleanField(required=False)
  tags = TagSerializer(many=True, read_only=True)
  status = serializers.ChoiceField(Video.STATUS_CHOICES, read_only=True)

  views_statistics = serializers.ReadOnlyField()
  shares_statistics = serializers.ReadOnlyField()

  class Meta:
    model = Video
    fields = Video.serialized
    depth = 1
