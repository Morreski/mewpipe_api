from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework import filters
from django.conf import settings
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


class VideoControllerSpecific(View):

  @csrf_exempt
  def dispatch(self, *args, **kwargs):
    return View.dispatch(self, *args, **kwargs)

  def get(self, request, uid):
    video = get_by_uid(Video, uid)
    if video is None:
      return JsonResponse({}, status=404)

    s = VideoSerializer(video)
    return JsonResponse(s.data)

  def put(self, request, uid):
    video = get_by_uid(Video, uid)
    if video is None:
      return JsonResponse({}, status=404)

    data = JSONParser().parse(request)
    serializer = VideoSerializer(video, data=data)

    if not serializer.is_valid():
      return JsonResponse(serializer.errors, status = 400)

    serializer.save()

    return JsonResponse(serializer.data)

  def delete(self, request, uid):
    video = get_by_uid(Video, uid)
    if video is None:
      return JsonResponse({}, status=404)

    video.delete()
    return JsonResponse({}, status=204)

class ShareController(View):

  @csrf_exempt
  def dispatch(self, *args, **kwargs):
    return View.dispatch(self, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    uid = kwargs.get("uid")
    video = get_by_uid(Video, uid)
    if video is None:
      return JsonResponse({}, status=404)

    data = JSONParser().parse(request)
    serializer = ShareSerializer(data=data)

    if not serializer.is_valid():
      return JsonResponse(serializer.errors, status=400)

    dests   = serializer.data.get('dest_addresses', [])
    sender  = serializer.data['sender_address']
    link    = serializer.data['video_link']

    video.share(sender, dests, link)

    s = VideoSerializer(video)
    return JsonResponse(s.data)
