from django.db import models
from django.db.models.aggregates import Sum
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
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
  watched = models.ManyToManyField('Video', through='View')

  def watch(self, video):
    view, created = self.view_set.get_or_create(video=video)
    view.update()


class TemporaryUser(User):
  ip = models.GenericIPAddressField(unpack_ipv4=True)


class UserAccount(User):
  pass
  """
  first_name = models.CharField(max_length = 100)
  last_name  = models.CharField(max_length = 100)
  birth_date = models.DateField()
  """


class Video(BaseModel):
  title = models.CharField(max_length = 40, db_index=True)
  description = models.TextField(blank=True)
  author = models.ForeignKey(User, null = True) #TODO: Remove null=true

  tags = models.ManyToManyField("Tag", through="VideoTag")

  total_view_count = models.IntegerField(default = 0)
  daily_view_count = models.IntegerField(default = 0)
  weekly_view_count = models.IntegerField(default = 0)
  monthly_view_count = models.IntegerField(default = 0)
  yearly_view_count = models.IntegerField(default = 0)

  total_share_count = models.IntegerField(default = 0)
  daily_share_count = models.IntegerField(default = 0)
  weekly_share_count = models.IntegerField(default = 0)
  monthly_share_count = models.IntegerField(default = 0)
  yearly_share_count = models.IntegerField(default = 0)

  watchers = models.ManyToManyField('User', through='View', related_name='watchers')

  serialized = BaseModel.serialized + (
      'title', 'author', 'tags', 'description',
      'total_view_count', 'daily_view_count', 'weekly_view_count', 'monthly_view_count', 'yearly_view_count',
      'total_share_count', 'daily_share_count', 'weekly_share_count', 'monthly_share_count', 'yearly_share_count',
  )

  search_indexes = ['title', 'description', 'tag__name']

  def share(self, sender, dest_list, link):
    mail = Mail.objects.get(name="videoSharing")
    mail.send(sender, dest_list, link=link)

    self.total_share_count += len(dest_list)
    self.save()

  @property
  def total_views(self):
    computed_views = self.view_set.all().aggregate(Sum('counter'))['counter__sum']
    return self.total_view_count + computed_views


class Tag(BaseModel):
  name = models.CharField(max_length=100, db_index=True, unique=True)
  videos = models.ManyToManyField("Video", through="VideoTag")

  serialized = BaseModel.serialized + ('name', 'videos')

  def save(self, *args, **kwargs):
    self.name = self.name.replace(' ', '')
    BaseModel.save(self, *args, **kwargs)

class Mail(BaseModel):
  name  = models.CharField(unique=True, max_length=255)
  subject = models.CharField(max_length=255)
  body_template = models.TextField()

  def send(self, sender, recipient_list, **kwargs):
    send_mail(
      self.subject,
      self.body_template.format(**kwargs),
      sender,
      recipient_list,
      )

class View(BaseModel):
  user  = models.ForeignKey(User)
  video = models.ForeignKey(Video)
  counter = models.IntegerField(default = 1)

  def update(self):
    if (timezone.now() - timezone.timedelta(minutes=settings.VIEW_TIMEOUT) ) < self.edition_date:
      return (self, False)
    self.counter += 1
    self.save()
    return (self, True)

  class Meta:
    unique_together = ( ('video', 'user'), )

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
