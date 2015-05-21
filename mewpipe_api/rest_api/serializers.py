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

class ShareSerializer(serializers.Serializer):
  sender_address = serializers.EmailField()
  dest_addresses = serializers.ListField(child=serializers.EmailField())
  video_link     = HtmlCleanField()

class VideoSerializer(serializers.ModelSerializer):
  title = HtmlCleanField(max_length=40)
  description = HtmlCleanField(required=False)
  tags = TagSerializer(many=True, read_only=True)

  total_view_count = serializers.IntegerField(read_only=True)
  daily_view_count = serializers.IntegerField(read_only=True)
  weekly_view_count = serializers.IntegerField(read_only=True)
  monthly_view_count = serializers.IntegerField(read_only=True)
  yearly_view_count = serializers.IntegerField(read_only=True)

  total_share_count = serializers.IntegerField(read_only=True)
  daily_share_count = serializers.IntegerField(read_only=True)
  weekly_share_count = serializers.IntegerField(read_only=True)
  monthly_share_count = serializers.IntegerField(read_only=True)
  yearly_share_count = serializers.IntegerField(read_only=True)

  class Meta:
    model = Video
    fields = Video.serialized
    depth = 1
