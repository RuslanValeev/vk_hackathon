from django.shortcuts import HttpResponse, redirect, render
from django.http import JsonResponse
import vk
from vkapp.settings import VK_ACCESS_TOKEN, VK_APP_CLIENT_ID
from .models import Client

def oauth(request):
    oauth_url = 'https://oauth.vk.com/authorize?client_id=' + VK_APP_CLIENT_ID + '&display=page&redirect_uri=localhost:8000&response_type=token&v=5.68'
    return(redirect(oauth_url))

def get_user_info(request):
    request_params = request.GET
    session = vk.Session(access_token=VK_ACCESS_TOKEN)
    vk_api = vk.API(session)

    response = {}
    response['group_id'] = request_params.get('group_id')
    response['api_settings'] = request_params.get('api_settings')

    user = {}
    user['id'] = request_params.get('viewer_id')
    user['is_app_user'] = request_params.get('is_app_user')
    user_info = vk_api.users.get(user_id=user['id'], fields='last_seen, first_name, last_name, country, city, photo_200')
    # account_info = vk_api.
    user['city'] = user_info[0]['city']
    user['name'] = user_info[0]['first_name'] + " " + user_info[0]['last_name']
    user['avatar_url'] = user_info[0]['photo_200']

    Client.objects.create(
        vk_id_ref=user['id'],
        name=user['name'],
        money=0,
        description='',
        avatar_url=user['avatar_url']
    )
    response['user'] = user


    # print(vk_api.account.getProfileInfo())

    return(JsonResponse(response))
