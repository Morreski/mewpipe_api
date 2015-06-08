from __future__ import absolute_import

from mewpipe_api.videoconverter import convert
from celery import shared_task

@shared_task
def task_convert(video, ext):
 convert(video, ext)
