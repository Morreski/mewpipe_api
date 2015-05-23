from django_extensions.management.jobs import WeeklyJob
from django.db.models import F
from rest_api.models import Video

class Job(WeeklyJob):
    help = "Compute video statistics => Weekly counts and share"

    def execute(self):
      Video.objects.all().update(
          weekly_view_count = F('total_view_count'),
          weekly_share_count = F('total_share_count'),
      )
