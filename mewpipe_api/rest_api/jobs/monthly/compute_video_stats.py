from django_extensions.management.jobs import MonthlyJob
from django.db.models import F
from rest_api.models import Video

class Job(MonthlyJob):
    help = "Compute video statistics => Monthly counts and share"

    def execute(self):
      Video.objects.all().update(
          monthly_view_count = F('total_view_count'),
          monthly_share_count = F('total_share_count'),
      )
