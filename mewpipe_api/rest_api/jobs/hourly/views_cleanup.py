from django_extensions.management.jobs import HourlyJob
from django.db.models import F
from django.conf import settings
from django.utils import timezone
from rest_api.models import View, Video

class Job(HourlyJob):
    help = "Remove all views and add them to videos counter"

    def execute(self):
      delta = timezone.timedelta(hours=settings.VIEW_TTL)
      deadline = timezone.now() - delta
      views = View.objects.filter(creation_date__lte = deadline)

      for view in views:
        Video.objects.filter(view=view).update(total_view_count=F('total_view_count') + view.counter)

        view.delete()
