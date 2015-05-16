from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_api.shortcuts import JsonResponse, get_by_uid
from rest_api.models import Video
from rest_api.serializers import VideoSerializer

from django.views.generic import View

class VideoControllerGeneral(View):

  @csrf_exempt
  def dispatch(self, *args, **kwargs):
    return View.dispatch(self, *args, **kwargs)

  def get(self, request):
    videos = Video.objects.all()
    serializer = VideoSerializer(videos, many=True)
    return JsonResponse(serializer.data)

  def post(self, request):
    data = JSONParser().parse(request)
    serializer = VideoSerializer(data=data)
    if not serializer.is_valid():
      return JsonResponse(serializer.errors, status = 400)

    serializer.save()

    return JsonResponse(serializer.data)

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

