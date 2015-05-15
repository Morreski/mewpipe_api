from django.db import models
from rest_api.shortcuts import generate_uuid
# Create your models here.

class BaseModel(models.Model):
  uid = models.UUIDField(default=generate_uuid, editable=False)
  creation_date = models.DateTimeField(auto_now_add=True)
  edition_date = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True

class User(BaseModel):
  pass

class Video(BaseModel):
  title = models.CharField(max_length = 40, db_index=True)
  author = models.ForeignKey(User, null = True) #TODO: Remove null=true

  tags = models.ManyToManyField("Tag", through="VideoTag")


class Tag(BaseModel):
  name = models.CharField(max_length=100, db_index=True, unique=True)
  videos = models.ManyToManyField("Video", through="VideoTag")

class VideoTag(BaseModel):
  SECONDARY = 0
  PRIMARY = 1

  LEVEL_CHOICES = (
    (SECONDARY, "Secondary"),
    (PRIMARY, "Primary")
  )

  tag = models.ForeignKey(Tag)
  video = models.ForeignKey(Video)
  tag_level = models.IntegerField(choices=LEVEL_CHOICES)


