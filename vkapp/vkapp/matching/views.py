from django.shortcuts import HttpResponse
from vkapp.matching.models import EventUser
from vkapp.people.models import Client
from vkapp.events.models import Event

def post_subscribe_user_to_event(request):
    user_id = request.POST.get("user_id")
    event_id = request.POST.get("event_id")
    client = Client.objects.get(vk_id_ref=user_id)
    event = Event.objects.get(afisha_event_ref=event_id)
    if client and event:
        EventUser.create(client, event)
    print(user_id, event_id)

    return HttpResponse(200)
