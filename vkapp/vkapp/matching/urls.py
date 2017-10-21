from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^subscribe', views.post_subscribe_user_to_event, name='post_subscribe'),
    url(r'^get_subscribers', views.get_subscribers, name='get_subscribers'),
    url(r'^get_matches', views.get_matches, name='get_matches'),
    url(r'^like', views.post_like, name='post_like'),
]
