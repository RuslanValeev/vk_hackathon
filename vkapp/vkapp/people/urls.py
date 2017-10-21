from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user', views.get_user_info, name='user_info'),
    url(r'^oauth', views.oauth, name='oauth'),
]
