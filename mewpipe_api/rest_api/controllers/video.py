from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import generics

from rest_api.shortcuts import JsonResponse, get_by_uid, normalize_query
from rest_api.models import Video, Tag, VideoTag
from rest_api.serializers import VideoSerializer, ShareSerializer
from rest_api.paginators import VideoPaginator

from django.views.generic import View

import watson

class VideoControllerGeneral(generics.ListCreateAPIView):

  serializer_class = VideoSerializer
  pagination_class = VideoPaginator
  queryset = Video.objects.all()

  def list(self, request, *args, **kwargs):
    search_string = request.GET.get('s', '')
    if search_string == '':
      return generics.ListCreateAPIView.list(self, request, *args, **kwargs)

    qs = self.filter_queryset(self.get_queryset()).values_list("uid", flat=True)
    matched_items, all_results = ([], [])

    for _str in normalize_query(search_string):
      all_results.extend(watson.search(_str))

    for result in set(all_results):
      if not result.object.uid in qs:
        continue
      matched_items.append(result.object)

    page = self.paginate_queryset(matched_items)
    page.sort(key = lambda x: x.total_view_count, reverse = True)

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
