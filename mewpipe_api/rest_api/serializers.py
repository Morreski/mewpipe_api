from rest_framework import serializers
from rest_api.models import Video, Tag
from rest_api.shortcuts import HtmlCleanField
from django.contrib.auth import get_user_model

class UserDetailsSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ('username', 'email', 'first_name', 'last_name')
    read_only_fields = ('email', )

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


class VideoSerializer(serializers.ModelSerializer):
  title = HtmlCleanField(max_length=40)
  description = HtmlCleanField(required=False, allow_blank=True)
  status = serializers.ChoiceField(Video.STATUS_CHOICES, read_only=True)

  tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
  views_statistics = serializers.ReadOnlyField()
  shares_statistics = serializers.ReadOnlyField()
  file_urls = serializers.ReadOnlyField()
  thumbnail_url = serializers.ReadOnlyField()
  hr_duration = serializers.ReadOnlyField()
  duration = serializers.IntegerField(read_only=True)


  class Meta:
    model = Video
    fields = Video.serialized
    depth = 1

