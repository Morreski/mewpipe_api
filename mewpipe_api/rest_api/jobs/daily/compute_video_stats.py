from django_extensions.management.jobs import DailyJob
from django.db.models import F
from rest_api.models import Video

class Job(DailyJob):
    help = "Compute video statistics => Daily counts and share"

    def execute(self):
      Video.objects.all().update(
          daily_view_count = F('total_view_count'),
          daily_share_count = F('total_share_count'),
      )
