from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models.aggregates import Sum
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
import os, uuid
# Create your models here.

class VideoManager(models.Manager):
  def get_queryset(self):
    qs = models.Manager.get_queryset(self)
    return qs.annotate(
        daily_share = models.F("total_share_count") - models.F("daily_share_count"),
        weekly_share = models.F("total_share_count") - models.F("weekly_share_count"),
        monthly_share = models.F("total_share_count") - models.F("monthly_share_count"),
        yearly_share = models.F("total_share_count") - models.F("yearly_share_count"),

        daily_view = models.F("total_view_count") - models.F("daily_view_count"),
        weekly_view = models.F("total_view_count") - models.F("weekly_view_count"),
        monthly_view = models.F("total_view_count") - models.F("monthly_view_count"),
        yearly_view = models.F("total_view_count") - models.F("yearly_view_count"),
    )


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

  @staticmethod
  def getUser(**kwargs):
    ip_address = kwargs.get('ip_address')
    if ip_address:
      return TemporaryUser.objects.get_or_create(ip=ip_address)[0]


class TemporaryUser(User):
  ip = models.GenericIPAddressField(unpack_ipv4=True, unique=True)

class CustomUserManager(BaseUserManager):
  use_in_migrations = True

  def _create_user(self, fname, lname, email, username, birth_date, **extra_fields):
    email = self.normalize_email(email)
    user = self.model(first_name=fname, last_name=lname, email=email, username=username, birth_date=birth_date, **extra_fields)
    user.save(using=self._db)
    return user

  def create_user(self, fname='None', lname='None', email='None', username='None', birth_date=None, **extra_fields):
    return self._create_user(fname, lname, email, username, birth_date,**extra_fields)

class UserAccount(User):
  first_name  = models.CharField(max_length = 100)
  last_name   = models.CharField(max_length = 100)
  email       = models.CharField(max_length = 100)
  username    = models.CharField(max_length = 100)
  birth_date  = models.DateTimeField(null=True)
  last_login  = models.DateTimeField(null=True)
  is_active   = models.BooleanField(default=True)

  objects = CustomUserManager()

  serialized = ('first_name', 'last_name', 'email', 'username', 'birth_date', 'is_active')

class Video(BaseModel):

  objects = VideoManager()

  STATUS_NEW = 0
  STATUS_UPLOADING = 1
  STATUS_UPLOADED = 2
  STATUS_READY = 3

  STATUS_CHOICES = (
    (STATUS_NEW, "New"),
    (STATUS_UPLOADING, "Uploading"),
    (STATUS_UPLOADED, "Uploaded"),
    (STATUS_READY, "Ready"),
  )

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

  status = models.IntegerField(default=0, choices=STATUS_CHOICES)

  serialized = BaseModel.serialized + (
      'title', 'author', 'tags', 'description', 'status', 'views_statistics', 'shares_statistics', 'file_urls',
  )

  search_indexes = ['title', 'description', 'tag__name']

  def share(self, sender, dest_list, link):
    mail = Mail.objects.get(name="videoSharing")
    mail.send(sender, dest_list, link=link)

    self.total_share_count += len(dest_list)
    self.save()

  def get_fileName(self, video_format):
    return str(self.uid) + "." + video_format

  @property
  def views_statistics(self):
    views = {}

    computed_views = self.view_set.all().aggregate(Sum('counter'))['counter__sum']
    if computed_views is None:
      computed_views = 0

    views["total"] = self.total_view_count + computed_views
    views["daily"] = views["total"] - self.daily_view_count
    views["weekly"] = views["total"] - self.weekly_view_count
    views["monthly"] = views["total"] - self.monthly_view_count
    views["yearly"] = views["total"] - self.yearly_view_count
    return views

  @property
  def shares_statistics(self):
    shares = {}

    shares["total"] = self.total_share_count
    shares["daily"] = shares["total"] - self.daily_share_count
    shares["weekly"] = shares["total"] - self.weekly_share_count
    shares["monthly"] = shares["total"] - self.monthly_share_count
    shares["yearly"] = shares["total"] - self.yearly_share_count
    return shares

  @property
  def file_urls(self):
    domain_name = settings.DOMAIN_NAME
    return [
        {
          "type" : "video/mp4",
          "src"  : "http://{domain_name}/api/videos/{uid}/download?video_format=mp4".format(domain_name=domain_name, uid=str(self.uid))
        }
    ]

  def writeOnDisk(self, file):

    upload_path = os.path.join(settings.UPLOAD_DIR, 'pending_videos', str(self.uid))

    if not os.path.exists(os.path.dirname(upload_path)):
        os.makedirs(os.path.dirname(upload_path))

    with open(upload_path, 'wb+') as videoFile:
        for chunk in file.chunks():
          videoFile.write(chunk)

    self.status = Video.STATUS_UPLOADED
    self.save()

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
