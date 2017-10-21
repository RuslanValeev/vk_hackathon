from django.db import models

# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=255)
    city_id = models.IntegerField()
    start_date = models.DateTimeField
    end_date = models.DateTimeField

    def __str__(self):
        return self.title
