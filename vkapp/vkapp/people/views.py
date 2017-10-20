from django.shortcuts import render
from django.shortcuts import HttpResponse
import vk

def people_index(request):
    return(HttpResponse("You are at people index"))

def get_user_info(request):
    session = vk.Session()
    vk_api=vk.API(session)
    user_id_get = request.GET.get('usr', '')
    user1 = vk_api.users.get(user_id=user_id_get, fields='last_seen')
    return(HttpResponse(user1))
