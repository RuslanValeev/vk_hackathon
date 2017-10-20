from django.shortcuts import HttpResponse
from django.http import JsonResponse
import vk
from vkapp.settings import VK_ACCESS_TOKEN

def people_index(request):
    return(HttpResponse("<html>You are at people index</html>"))

def get_user_info(request):
    request_params = request.GET

    session = vk.Session(access_token=VK_ACCESS_TOKEN)
    vk_api = vk.API(session)

    response = {}
    response['group_id'] = request_params.get('group_id')
    response['api_settings'] = request_params.get('api_settings')

    user = {}
    user['id'] = int(request_params.get('viewer_id'))
    user['is_app_user'] = request_params.get('is_app_user')
    user_info = vk_api.users.get(user_id=user['id'], fields='last_seen, first_name, last_name, country, city, photo_200')
    # account_info = vk_api.
    user['city'] = user_info[0]['city']
    user['name'] = user_info[0]['first_name'] + " " + user_info[0]['last_name']
    user['avatar_url'] = user_info[0]['photo_200']
    response['user'] = user
    # print(vk_api.account.getProfileInfo())

    return(JsonResponse(response))
