from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.html import strip_tags
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import CharField
from hashlib import md5
from django.db.models import Q
import uuid, re

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

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()).lower() for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string).sort()
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query, terms

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
