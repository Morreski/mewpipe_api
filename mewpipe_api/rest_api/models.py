from django.db import models
import uuid
# Create your models here.

class BaseModel(models.Model):
  uid = models.UUIDField(default=uuid.uuid4, editable=False)
  creation_date = models.DateTimeField(auto_now_add=True)
  edition_date = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True

  serialized = ('uid', 'creation_date', 'edition_date')


class User(BaseModel):
  pass

class Video(BaseModel):
  title = models.CharField(max_length = 40, db_index=True)
  description = models.TextField(blank=True)
  author = models.ForeignKey(User, null = True) #TODO: Remove null=true

  tags = models.ManyToManyField("Tag", through="VideoTag")

  serialized = BaseModel.serialized + ('title', 'author', 'tags', 'description')

class Tag(BaseModel):
  name = models.CharField(max_length=100, db_index=True, unique=True)
  videos = models.ManyToManyField("Video", through="VideoTag")

  serialized = BaseModel.serialized + ('name', 'videos')

  def save(self, *args, **kwargs):
    self.name = self.name.replace(' ', '')
    BaseModel.save(self, *args, **kwargs)

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

  serialized = BaseModel.serialized + ('tag', 'video', 'tag_level')

