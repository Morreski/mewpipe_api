from rest_framework import generics
from rest_framework import parsers
from rest_framework import filters
from rest_framework.views import APIView

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import StreamingHttpResponse
from django.core.files import File

from rest_api.shortcuts import JsonResponse, get_by_uid, normalize_query
from rest_api.models import Video, Tag, VideoTag
from rest_api.serializers import VideoSerializer, ShareSerializer
from rest_api.paginators import VideoPaginator

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
      'daily_view_count',
      'weekly_view_count',
      'monthly_view_count',
      'yearly_view_count',

      'total_share_count',
      'daily_share_count',
      'monthly_share_count',
      'weekly_share_count',
      'yearly_share_count',
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
    for tagName in request.data.get('tags', []):
      self.tagNames.append(tagName)
    return generics.ListCreateAPIView.post(self, request, *args, **kwargs)

  def perform_create(self, serializer):
    v = serializer.save()
    for tagName in self.tagNames:
      t, created = Tag.objects.get_or_create(name=tagName)
      VideoTag.objects.create(tag=t,video=v, tag_level=0)


class VideoControllerSpecific(generics.RetrieveUpdateDestroyAPIView):

  queryset = Video.objects.all()
  serializer_class = VideoSerializer
  lookup_field = 'uid'


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

  def post(self, request, *args, **kwargs):
    uid = kwargs['uid']
    video = get_by_uid(Video, uid)
    if video is None:
      return JsonResponse({}, status = 404)

    if video.status != Video.STATUS_NEW:
      return JsonResponse({}, status = 404)

    video.status = Video.STATUS_UPLOADING
    video.save()

    file = request.data.get('file')
    if file is None:
      return JsonResponse({"file" : "Field Required"}, status=400)

    if file._size > settings.VIDEO_SIZE_LIMIT:
      return JsonResponse({"file" : "Video size too large"}, status=413)

    video.writeOnDisk(file)

    return JsonResponse({})

class DownloadVideoController(APIView):

  def get(self, request, *args, **kwargs):
    video_format = request.GET.get('video_format', "mp4")

    if video_format not in settings.SUPPORTED_VIDEO_FORMATS:
      return StreamingHttpResponse({"Video Format Error" : settings.SUPPORTED_VIDEO_FORMATS }, status=400)

    uid = kwargs['uid']
    video = get_by_uid(Video, uid)

    if video is None:
      return StreamingHttpResponse({}, status=404)

    if video.status != Video.STATUS_READY:
      return StreamingHttpResponse({}, status=403)

    file = video.get_file(video_format)
    wrapper = File(file)
    response =  StreamingHttpResponse(wrapper, )
    response['Content-Type'] = "video/{0}".format(video_format)
    response['Content-Disposition'] = 'inline; filename="{0}.{1}"'.format(uid, video_format)
    return response
