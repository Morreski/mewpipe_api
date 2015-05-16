from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import generics

from rest_api.shortcuts import JsonResponse, get_by_uid
from rest_api.models import Video, Tag, VideoTag
from rest_api.serializers import VideoSerializer

from django.views.generic import View

class VideoControllerGeneral(generics.ListCreateAPIView):

  queryset = Video.objects.all()
  serializer_class = VideoSerializer

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

