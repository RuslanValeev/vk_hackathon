from django.db import models
from vkapp.events.models import Event
from vkapp.people.models import Client


# Create your models here.
class EventUser(models.Model):
    afisha_event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    vk_user = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.afisha_event + " – " + self.vk_user

