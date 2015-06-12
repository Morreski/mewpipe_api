from __future__ import absolute_import

from rest_api.videoconverter import convert, extract_thumbnails_and_datas
from celery import shared_task

@shared_task
def task_thumbnails(video, ext):
  extract_thumbnails_and_datas(video, ext)

@shared_task
def task_convert(video, ext):
 convert(video, ext)

