from django.db import models
from vkapp.events.models import Event
from vkapp.people.models import Client
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests


class EventUser(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    class Meta:
        unique_together = [
            ('event', 'client')
        ]

    def __str__(self):
        return(self.event.__str__() + " – " + self.client.__str__())


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


@receiver(post_save, sender=Match, dispatch_uid="send_messages")
def send_messages(sender, instance, update_fields, created, **kwargs):
    print('here')
    # r = requests.post('https://api.vk.com/method/users.get', data={'user_ids': '210700286', 'fields': 'bdate', 'v': '5.68'})
    # print(r.text)