from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import serializers

from rest_api.models import Video, Tag
from rest_api.shortcuts import HtmlCleanField

class PasswordChangeSerializer(serializers.Serializer):

  old_password = serializers.CharField(max_length=128)
  new_password1 = serializers.CharField(max_length=128)
  new_password2 = serializers.CharField(max_length=128)

  set_password_form_class = SetPasswordForm

  def __init__(self, *args, **kwargs):
    self.old_password_field_enabled = getattr(
      settings, 'OLD_PASSWORD_FIELD_ENABLED', False
    )
    super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

    if not self.old_password_field_enabled:
      self.fields.pop('old_password')

    self.request = self.context.get('request')
    self.user = getattr(self.request, 'user', None)

  def validate_old_password(self, value):
    invalid_password_conditions = (
      self.old_password_field_enabled,
      self.user,
      not self.user.check_password(value)
    )

    if all(invalid_password_conditions):
      raise serializers.ValidationError('Invalid password')
    return value

  def validate(self, attrs):
    self.set_password_form = self.set_password_form_class(
      user=self.user, data=attrs
    )

    if not self.set_password_form.is_valid():
      raise serializers.ValidationError(self.set_password_form.errors)
    return attrs

  def save(self):
    self.set_password_form.save()

class UserDetailsSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ('username', 'email', 'first_name', 'last_name')
    read_only_fields = ('email', )

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