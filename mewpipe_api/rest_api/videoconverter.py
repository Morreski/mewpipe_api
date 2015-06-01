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
  thumbnail_path = os.path.join(settings.UPLOAD_DIR, "thumbnails", name + "_%d.jpg")


  if not os.path.exists(os.path.dirname(output_path)):
      os.makedirs(os.path.dirname(output_path))
  if not os.path.exists(os.path.dirname(thumbnail_path)):
      os.makedirs(os.path.dirname(thumbnail_path))

  thumb_command = "avconv -i {input} -vf fps=1 {output} -loglevel quiet".format(
    input = input_path,
    output = thumbnail_path
  )
  Popen(thumb_command, shell=True)

  for extension in settings.SUPPORTED_VIDEO_FORMATS:
    command = "avconv -y -i {input} -strict experimental {output} -loglevel quiet".format(
      input = input_path,
      output = output_path + "." + extension
    )
    Popen(command, shell=True)

  #FIXME: DEBUG
  video.status = video.STATUS_READY
  video.save()
