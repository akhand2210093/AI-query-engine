from django.db import models

# Create your models here.

from django.db import models

class SalesData(models.Model):
    month = models.CharField(max_length=20)
    revenue = models.IntegerField()

    def __str__(self):
        return f"{self.month}: {self.revenue}"

