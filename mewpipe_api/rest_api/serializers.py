from rest_framework import serializers
from rest_api.models import Video
from rest_api.shortcuts import HtmlCleanField

class VideoSerializer(serializers.ModelSerializer):
  title = HtmlCleanField(max_length=40)
  description = HtmlCleanField()

  class Meta:
    model = Video
    fields = Video.serialized
