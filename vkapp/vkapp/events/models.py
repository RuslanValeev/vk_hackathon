from django.db import models

# Create your models here.


class Event(models.Model):
    afisha_event_ref = models.CharField(max_length=16)
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=255)
    city_id = models.IntegerField()
    start_date = models.CharField(max_length=30, null=True)
    end_date = models.CharField(max_length=30, null=True)

    def __str__(self):
        return(self.title)
