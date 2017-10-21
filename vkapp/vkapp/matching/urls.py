from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^post/subscribe', views.post_subscribe_user_to_event, name='post_subscribe'),
]
