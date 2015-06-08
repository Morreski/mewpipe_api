from __future__ import absolute_import
from celery import Celery
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mewpipe_api.settings')

app = Celery('mewpipe_api')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
  CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
)


