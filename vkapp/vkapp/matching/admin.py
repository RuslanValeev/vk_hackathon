from django.contrib import admin

from .models import EventUser, Like, Match

admin.site.register(EventUser)
admin.site.register(Like)
admin.site.register(Match)
