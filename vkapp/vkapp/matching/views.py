from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
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
    user_id = request.GET.get("user_id")
    filter = str(request.GET.get("filter")).lower()

    do_filter = False

    if filter == "true":
        do_filter = True

    current_user = Client.objects.get(vk_id_ref=user_id)

    event_ = Event.objects.get(afisha_event_ref=event_id)

    non_display_users = []

    likes = Like.objects.filter(active_client=current_user, event=event_)

    for like_entity in likes:
        non_display_users.append(like_entity.passive_client.vk_id_ref)

    response = {}
    users = []
    event_user_entities = EventUser.objects.filter(event=event_)

    for entity in event_user_entities:
        if entity.client.vk_id_ref in non_display_users and do_filter:
            pass
        else:
            users.append(int(entity.client.vk_id_ref))
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
    response = {'match_created': False}
    if active_client_entity and passive_client_entity and event_entity:
        like_entity = Like.objects.get_or_create(active_client=active_client_entity, passive_client=passive_client_entity, event=event_entity, mark=like)
        if Like.objects.filter(active_client=passive_client_entity, passive_client=active_client_entity, event=event_entity).exists():
            response['match_created'] = True
            if not Match.objects.filter(event=event_entity, client_2=active_client_entity, client_1=passive_client_entity).exists()\
                    or Match.objects.filter(event=event_entity, client_1=active_client_entity, client_2=passive_client_entity).exists():
                match_entity = Match.objects.get_or_create(event=event_entity, client_1=active_client_entity, client_2=passive_client_entity)
        return(JsonResponse(response))
    else:
        return(HttpResponse(500))

def get_matches(request):
    user_id = request.GET.get('user_id')
    client_instance = Client.objects.get(vk_id_ref=user_id)
    matches_queryset = Match.objects.filter(
        Q(client_1=client_instance) | Q(client_2=client_instance)
    )
    pre_response = {}
    for match_entity in matches_queryset:
        current_match_event_key = str(match_entity.event.afisha_event_ref)
        pre_response[current_match_event_key] = set()

    for match_entity in matches_queryset:
        current_match_event_key = str(match_entity.event.afisha_event_ref)
        pre_response[current_match_event_key].add(match_entity.client_1.vk_id_ref)
        pre_response[current_match_event_key].add(match_entity.client_2.vk_id_ref)
        pre_response[current_match_event_key].remove(client_instance.vk_id_ref)

    response = {}
    for key, value in pre_response.items():
        response[key] = list(value)

    return JsonResponse(response)
