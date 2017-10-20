from django.shortcuts import render
from django.shortcuts import HttpResponse
import vk

def people_index(request):
    return(HttpResponse("You are at people index"))

def get_user_info(request):
    session = vk.Session()
    vk_api=vk.API(session)
    user_id_get = request.GET.get('usr', '')
    request_params = request.GET
    viewer_id = request_params.get('viewer_id')
    group_id = request_params.get('group_id')
    user1 = vk_api.users.get(user_id=user_id_get, fields='last_seen')
    return(HttpResponse(user1))
