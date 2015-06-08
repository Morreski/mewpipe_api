from rest_framework import generics
from rest_framework import parsers
from rest_framework import filters
from rest_framework.views import APIView

from django.db.transaction import atomic
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse

from rest_api.shortcuts import JsonResponse, get_by_uid, normalize_query
from rest_api.models import Video, Tag, VideoTag, User
from rest_api.serializers import VideoSerializer, ShareSerializer
from rest_api.paginators import VideoPaginator
from rest_api.tasks import task_convert

from django.views.generic import View
import itertools


class VideoControllerGeneral(generics.ListCreateAPIView):

  serializer_class = VideoSerializer
  pagination_class = VideoPaginator
  filter_backends = (filters.OrderingFilter, )
  filter_fields = (
      'tag__name',
      'title',
      'creation_date',
      'edition_date',
      'total_view_count',
      'daily_view',
      'weekly_view',
      'monthly_view',
      'yearly_view',

      'total_share_count',
      'daily_share',
      'monthly_share',
      'weekly_share',
      'yearly_share',
  )
  ordering_fields = filter_fields
  queryset = Video.objects.all()


  def list(self, request, *args, **kwargs):
    search_string = request.GET.get('s', '')
    if search_string == '':
      return generics.ListCreateAPIView.list(self, request, *args, **kwargs)

    qs = self.get_queryset()

    match_sentences, match_tags, match_words = ([], [], [])
    terms = normalize_query(search_string)
    for index,term in enumerate(terms):
      grouped_terms = terms[0:] if index == 0 else terms[0:-index]
      big_term = ''.join(grouped_terms)
      match_sentences.extend(list(qs.filter(title__icontains=big_term)))

    for term in terms:
      match_words.extend(list(qs.filter(title__icontains=term)))

    for term in terms:
      match_tags.extend(list(qs.filter(tag__name__icontains=term)))

    matched_items = list(itertools.chain(match_sentences, match_words, match_tags))[:settings.VIDEO_PAGINATION_LIMIT]
    videos = sorted(set(matched_items), key=lambda x: matched_items.index(x))
    page = self.paginate_queryset(videos)

    s = self.get_serializer(page, many=True)
    return self.get_paginated_response(s.data)

  def __init__(self, *args, **kwargs):
    self.tagNames = []
    generics.ListCreateAPIView.__init__(self, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    for tagName in request.data.get('tags', [])[:10]:
      self.tagNames.append(tagName)
    return generics.ListCreateAPIView.post(self, request, *args, **kwargs)

  def perform_create(self, serializer):
    v = serializer.save()
    for tagName in self.tagNames:
      tagName = tagName.replace(' ', '').lower()
      t, created = Tag.objects.get_or_create(name=tagName)
      VideoTag.objects.create(tag=t,video=v, tag_level=0)


class VideoControllerSpecific(generics.RetrieveUpdateDestroyAPIView):

  queryset = Video.objects.all()
  serializer_class = VideoSerializer
  lookup_field = 'uid'

  def perform_update(self, serializer):
    v = serializer.save()
    tagNames = self.request.data.get("tags")
    if tagNames is None:
      return

    VideoTag.objects.filter(video=v).delete()
    for tagName in tagNames[:10]:
      tagName = tagName.replace(' ', '').lower()
      t, created = Tag.objects.get_or_create(name=tagName)
      VideoTag.objects.create(tag=t,video=v, tag_level=0)

class ShareController(View):

  @csrf_exempt
  def dispatch(self, *args, **kwargs):
    return View.dispatch(self, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    uid = kwargs.get("uid")
    video = get_by_uid(Video, uid)
    if video is None:
      return JsonResponse({}, status=404)

    data = parsers.JSONParser().parse(request)
    serializer = ShareSerializer(data=data)

    if not serializer.is_valid():
      return JsonResponse(serializer.errors, status=400)

    dests   = serializer.data.get('dest_addresses', [])
    sender  = serializer.data['sender_address']
    link    = serializer.data['video_link']

    video.share(sender, dests, link)

    s = VideoSerializer(video)
    return JsonResponse(s.data)

class UploadVideoController(APIView):
  parsers = (parsers.FileUploadParser )

  @atomic
  def post(self, request, *args, **kwargs):
    uid = kwargs['uid']
    video = get_by_uid(Video, uid)
    if video is None:
      return JsonResponse({}, status = 404)

    if video.status != Video.STATUS_NEW:
      return JsonResponse({}, status = 403)

    video.status = Video.STATUS_UPLOADING
    video.save()

    filename = request.FILES[request.FILES.keys()[0]].name #get only first file in request
    ext = filename.strip().split('.')[-1]
    file = request.data.get('file')

    if file is None:
      return JsonResponse({"file" : "Field Required"}, status=400)

    if file._size > settings.VIDEO_SIZE_LIMIT:
      return JsonResponse({"file" : "Video size too large"}, status=413)

    video.writeOnDisk(file, ext)
    task_convert.delay(video, ext)

    return JsonResponse({})


class ThumbnailVideoController(APIView):

  def get(self, request, *args, **kwargs):
    uid = kwargs['uid']

    try:
      time = int(self.request.GET.get('t'))
    except:
      time = 0

    video = get_by_uid(Video, uid)

    if video is None:
      return HttpResponse({}, status=404)

    if video.status != Video.STATUS_READY:
      return HttpResponse({}, status=403)

    if not time:
      time = video.thumbnail_frame

    filename = "{uid}_{number}.jpg".format(
      uid = str(video.uid),
      number = time + 1 #+1 cause of ffmpeg output
    )

    response = HttpResponse()
    response['Content-Type'] = "image/jpg"
    response['Content-Disposition'] = 'inline; filename="{0}"'.format(filename)
    response['X-Accel-Redirect'] = "/thumbnails/{filename}".format(filename=filename)
    return response


class DownloadVideoController(APIView):

  def get(self, request, *args, **kwargs):
    video_format = request.GET.get('video_format', "mp4")

    if video_format not in settings.SUPPORTED_VIDEO_FORMATS:
      return HttpResponse({"Video Format Error" : settings.SUPPORTED_VIDEO_FORMATS }, status=400)

    uid = kwargs['uid']
    video = get_by_uid(Video, uid)

    if video is None:
      return HttpResponse({}, status=404)

    if video.status != Video.STATUS_READY:
      return HttpResponse({}, status=400)

    ip_address = request.META['REMOTE_ADDR']
    temp_user = User.getUser(ip_address=ip_address)
    temp_user.watch(video)

    filename = video.get_fileName(video_format)
    response = HttpResponse()
    response['Content-Type'] = "video/{0}".format(video_format)
    response['Content-Disposition'] = 'inline; filename="{0}.{1}"'.format(uid, video_format)
    response['X-Accel-Redirect'] = "/videos/{filename}".format(filename=filename)
    return response
