from django.db import models

class EventUser(models.Model):
    afisha_event = models.CharField(max_length=16)
    vk_user = models.IntegerField(max_length=32)
