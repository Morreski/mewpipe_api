from django.conf import settings
from subprocess import check_output
from django.dispatch import Signal
from datetime import timedelta
import os, json

video_ready = Signal(providing_args = ["video", "ext"])

def get_video_metadatas(video_path):
  out = check_output("exiftool -j %s" % video_path, shell=True)
  return json.loads(out)[0]

def convert(video, ext, **kwargs):
  name = str(video.uid)
  input_path = os.path.join(settings.UPLOAD_DIR, "pending_videos", name + '.' + ext)
  output_path = os.path.join(settings.UPLOAD_DIR, "videos", name)
  thumbnail_path = os.path.join(settings.UPLOAD_DIR, "thumbnails", name + "_%d.jpg")


  if not os.path.exists(os.path.dirname(output_path)):
      os.makedirs(os.path.dirname(output_path))
  if not os.path.exists(os.path.dirname(thumbnail_path)):
      os.makedirs(os.path.dirname(thumbnail_path))

  video_metadatas = get_video_metadatas(input_path)

  #This method is getting uglier everydays thanks to exiftools >:(
  default_duration = "00:00:00"
  try:
    hms = map(int, video_metadatas.get("Duration", default_duration).split(":")) #format output as array of integers

    delta = timedelta(
      hours = hms[0],
      minutes = hms[1],
      seconds = hms[2]
    )
    total_seconds = delta.seconds

  except:
    total_seconds = int(video_metadatas.get("Duration", "00.00 s").split(".")[0])

  thumb_command = "avconv -i {input} -vf fps=1 {output} -loglevel quiet".format(
    input = input_path,
    output = thumbnail_path
  )
  check_output(thumb_command, shell=True)

  for extension in settings.SUPPORTED_VIDEO_FORMATS:
    command = "avconv -y -i {input} -strict experimental {output} -loglevel quiet".format(
      input = input_path,
      output = output_path + "." + extension
    )
    check_output(command, shell=True)

  #FIXME: DEBUG
  video.status = video.STATUS_READY
  video.duration = total_seconds
  video.save()
