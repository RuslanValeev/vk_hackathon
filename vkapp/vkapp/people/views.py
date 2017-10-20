from django.shortcuts import render
from django.shortcuts import HttpResponse
import vk, json

def people_index(request):
    return(HttpResponse("<html>You are at people index</html>"))

def get_user_info(request):
    request_params = request.GET

    session = vk.Session()
    vk_api = vk.API(session)

    response = {}
    response['group_id'] = request_params.get('group_id')
    response['api_settings'] = request_params.get('api_settings')

    user = {}
    user['id'] = int(request_params.get('viewer_id'))
    user['is_app_user'] = request_params.get('is_app_user')
    user_info = vk_api.users.get(user_id=user['id'], fields='last_seen, first_name, last_name, country, city, photo_200')
    user[''] = user_info[0]['city']
    response['user'] = user

    res_json = json.dumps(response)

    return(HttpResponse(res_json))
