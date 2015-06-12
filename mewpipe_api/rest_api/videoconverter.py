from django.conf import settings
from subprocess import check_output
from django.dispatch import Signal
from datetime import timedelta
import os, json

video_ready = Signal(providing_args = ["video", "ext"])

def get_video_metadatas(video_path):
  out = check_output("exiftool -j %s" % video_path, shell=True)
  return json.loads(out)[0]

def extract_thumbnails_and_datas(video, ext):
  name = str(video.uid)
  input_path = os.path.join(settings.UPLOAD_DIR, "pending_videos", name + '.' + ext)
  thumbnail_path = os.path.join(settings.UPLOAD_DIR, "thumbnails", name + '_')

  if not os.path.exists(os.path.dirname(thumbnail_path)):
      os.makedirs(os.path.dirname(thumbnail_path))

  video_metadatas = get_video_metadatas(input_path)

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

  if total_seconds == 0:
    return

  if total_seconds < settings.THUMBNAIL_COUNT:
    frames = total_seconds
    fps = 1
  else:
    frames = settings.THUMBNAIL_COUNT
    fps = total_seconds / frames

  for i in range(0, frames+1):
    thumb_command = "avconv -ss {position} -i {input} -vframes 1 {output} -loglevel quiet".format(
      position = i*fps,
      input = input_path,
      output = thumbnail_path + str(i+1) + '.jpg'
    )
    check_output(thumb_command, shell=True)

  video.duration = total_seconds
  video.save()

def convert(video, ext, **kwargs):
  name = str(video.uid)
  input_path = os.path.join(settings.UPLOAD_DIR, "pending_videos", name + '.' + ext)
  output_path = os.path.join(settings.UPLOAD_DIR, "videos", name)

  if not os.path.exists(os.path.dirname(output_path)):
      os.makedirs(os.path.dirname(output_path))

  for extension in settings.SUPPORTED_VIDEO_FORMATS:
    acodec_arg = ''
    if ext == extension:
      acodec_arg = '-acodec copy'

    command = "avconv -y -i {input} -strict experimental {acodec} {output} -loglevel quiet".format(
      input  = input_path,
      output = output_path + "." + extension,
      acodec = acodec_arg
    )
    check_output(command, shell=True)

  video.status = video.STATUS_READY
  video.save(update_fields=["status"]) #avoid conccurency problems by updating only one field
