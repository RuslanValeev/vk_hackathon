from django.shortcuts import HttpResponse
from django.http import JsonResponse
from vkapp.matching.models import EventUser
from vkapp.people.models import Client
from vkapp.events.models import Event

def post_subscribe_user_to_event(request):
    user_id = request.POST.get("user_id")
    event_id = request.POST.get("event_id")
    client = Client.objects.get(vk_id_ref=user_id)
    event = Event.objects.get(afisha_event_ref=event_id)
    if client and event:
        event = EventUser.objects.create(client=client, event=event)

    return HttpResponse(200)

def get_subscribers(request):
    event_id = request.GET.get("event_id")
    event_ = Event.objects.get(afisha_event_ref=event_id)
    response = {}
    users = []
    user_entities = EventUser.objects.filter(event=event_)
    for entity in user_entities:
        users.append(int(entity.client.vk_id_ref))
    print(user_entities)
    response['users'] = users
    return JsonResponse(response)
