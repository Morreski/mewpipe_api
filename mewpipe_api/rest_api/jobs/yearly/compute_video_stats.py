from django_extensions.management.jobs import YearlyJob
from django.db.models import F
from rest_api.models import Video

class Job(YearlyJob):
    help = "Compute video statistics => Daily counts and share"

    def execute(self):
      Video.objects.all().update(
          yearly_view_count = F('total_view_count'),
          yearly_share_count = F('total_share_count'),
      )
