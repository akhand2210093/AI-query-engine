from django.core.management.base import BaseCommand
from query.models import SalesData

class Command(BaseCommand):
    help = "Load mock sales data"

    def handle(self, *args, **kwargs):
        SalesData.objects.all().delete()  # Clear existing data
        SalesData.objects.create(month="last_month", revenue=250000)
        SalesData.objects.create(month="this_month", revenue=300000)
        self.stdout.write(self.style.SUCCESS("Mock data loaded successfully"))
