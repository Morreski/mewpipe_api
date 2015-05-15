from django.core.exceptions import ObjectDoesNotExist
from .exceptions import InternalError
from hashlib import md5
import uuid

def get_by_code(Model, code):
  try:
    return Model.objects.get(code=code)
  except ObjectDoesNotExist:
    return None

def update_object(obj, dict_fields, *locked_fields):
  locked_fields = locked_fields + tuple(['id', 'code'])

  for k,v in dict_fields.iteritems():
    if k not in obj._meta.get_all_field_names():
      raise InternalError("UNKNOWN_FIELD", "Unknown field {field} for the object {obj}", field=k, obj=obj._meta.model_name.title())

    if k in locked_fields:
      raise InternalError("FORBIDDEN_ACCESS", "You are not allowed to edit the field: '{field}'", field=k)

    obj.__dict__[k] = v

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

def generate_uuid():
  return uuid.uuid4().hex

def generate_link(filepath):
  return filepath #TODO: Determine link generation strategy

def generate_hash(path):
  return uuid.uuid5(uuid.NAMESPACE_URL, path).hex

def date_to_str(date):
  return date.strftime('%d/%m/%Y %H:%M:%S')
