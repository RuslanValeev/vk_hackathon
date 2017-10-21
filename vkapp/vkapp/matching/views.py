from django.shortcuts import HttpResponse
from django.http import JsonResponse
from .models import EventUser, Match, Like
from vkapp.people.models import Client
from vkapp.events.models import Event

def post_subscribe_user_to_event(request):
    user_id = request.POST.get("user_id")
    event_id = request.POST.get("event_id")
    client_entity = Client.objects.get(vk_id_ref=user_id)
    event_entity = Event.objects.get(afisha_event_ref=event_id)
    if client_entity and event_entity:
        event_entity = EventUser.objects.get_or_create(client=client_entity, event=event_entity)

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

def post_like(request):
    user_id = request.POST.get('user_id')
    subject_id = request.POST.get('subject_id')
    event_id = request.POST.get('event_id')
    like = request.POST.get('like')
    active_client_entity = Client.objects.get(vk_id_ref=user_id)
    passive_client_entity = Client.objects.get(vk_id_ref=subject_id)
    event_entity = Event.objects.get(afisha_event_ref=event_id)
    if active_client_entity and passive_client_entity and event_entity:
        Like.objects.get_or_create(active_client=active_client_entity, passive_client=passive_client_entity, event=event_entity)
        return(HttpResponse(200))
    else:
        return(HttpResponse(500))