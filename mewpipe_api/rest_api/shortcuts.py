from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.html import strip_tags
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import CharField
from hashlib import md5
import uuid

def get_by_uid(Model, uid):
  try:
    return Model.objects.get(uid=uid)
  except ObjectDoesNotExist:
    return None

class HtmlCleanField(CharField):

  def to_internal_value(self, data):
    value = CharField.to_internal_value(self, data)
    value = strip_tags(value)
    return value


def compute_md5(image_file):
    emdaicink = md5()
    image_file.seek(0)
    while 1:
      chunk = image_file.read(8192)
      if len(chunk) <= 0:
        break
      emdaicink.update(chunk)
    return emdaicink.hexdigest()

def file_upload_to(instance, filename):
  name, extension = filename.rsplit(".", 1)
  return str.join('/', [instance.directory.get_full_path(), instance.code + '.' + extension])
  #return os.path.join(instance.directory.get_full_path(), instance.code + '.' + extension)

class JsonResponse(HttpResponse):
  def __init__(self, data, **kwargs):
    content = JSONRenderer().render(data)
    kwargs["content_type"] = 'application/json'
    HttpResponse.__init__(self, content, **kwargs)

def generate_uuid():
  return uuid.uuid4().hex

def generate_link(filepath):
  return filepath #TODO: Determine link generation strategy

def generate_hash(path):
  return uuid.uuid5(uuid.NAMESPACE_URL, path).hex

def date_to_str(date):
  return date.strftime('%d/%m/%Y %H:%M:%S')
