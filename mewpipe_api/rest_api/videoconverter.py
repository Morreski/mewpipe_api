from django.conf import settings
from subprocess import Popen
from django.dispatch import receiver, Signal
import os

video_ready = Signal(providing_args = ["video", "ext"])

@receiver(video_ready)
def convert(video, ext, **kwargs):
  name = str(video.uid)
  input_path = os.path.join(settings.UPLOAD_DIR, "pending_videos", name + '.' + ext)
  output_path = os.path.join(settings.UPLOAD_DIR, "videos", name)

  if not os.path.exists(os.path.dirname(output_path)):
      os.makedirs(os.path.dirname(output_path))

  for extension in settings.SUPPORTED_VIDEO_FORMATS:
    command = "ffmpeg -y -i {input} {output} -loglevel quiet".format(
      input = input_path,
      output = output_path + "." + extension
    )
    Popen(command, shell=True)

  #FIXME: DEBUG
  video.status = video.STATUS_READY
  video.save()
