from django.shortcuts import render
from vkapp.matching.models import EventUser

def post_subscribe_user_to_event(request):
    user_id = request.POST.get("user_id")
    event_id = request.POST.get("event_id")
    #debug
    print(user_id, event_id)
    
