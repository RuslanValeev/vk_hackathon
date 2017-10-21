from django.db import models
from vkapp.events.models import Event
from vkapp.people.models import Client


# Create your models here.
class EventUser(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return(self.event + " – " + self.client)

    @classmethod
    def create(cls, user, event):
        event_user = cls(client=user, event=event)
        return event_user

class Match(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    client_1 = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='%(class)s_first_client')
    client_2 = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='%(class)s_second_client')

    def __str__(self):
        return(self.event + ": " + self.client_1 + " - " + self.client_2)

class Like(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    active_client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='%(class)s_active_client')
    passive_client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='%(class)s_passive_client')