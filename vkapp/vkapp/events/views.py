from django.shortcuts import render, redirect
from .models import Event as ModelEvent
from vkapp.people.models import Client
from vkapp.matching.models import EventUser
# Create your views here.

import xml.etree.ElementTree as ET
from django.http import JsonResponse
from vkapp.settings import XMLFILES_FOLDER
import json
import re

class Creation:
    creationId = ""
    name = ""
    url = ""
    description = ""
    editorialComment = ""
    synopsis = ""
    image_url = ""

class Schedule:
    creationId = ""
    begin = ""
    end = ""

class Likes:
    user_liked = False
    counter = 0

class Event:
    creation = Creation()
    schedule = Schedule()
    likes = Likes()

    def createEventDict(self):
        dict = {}
        dict["creation_id"] = self.creation.creationId
        dict["begin"] = self.schedule.begin
        dict["end"] = self.schedule.end
        dict["name"] = self.creation.name
        dict["url"] = self.creation.url
        dict["description"] = self.creation.description
        dict["editorial_comment"] = self.creation.editorialComment
        dict["synopsis"] = self.creation.synopsis
        dict["image_url"] = self.creation.image_url
        dict["likes_counter"] = self.likes.counter
        dict["is_liked"] = self.likes.user_liked
        return dict

    def __eq__(self, other):
        return self.creation.creationId == other.creation.creationId

    def __hash__(self):
        return hash(('creationId', self.creation.creationId))

def getTypeOfEvent(event_id):
    types = {
        'movie': re.compile('^movie', re.IGNORECASE),
        'performance': re.compile('^performance', re.IGNORECASE),
        'exhibition': re.compile('^exhibition', re.IGNORECASE),
        'concert': re.compile('^concert', re.IGNORECASE)
    }
    for type, regex in types.items():
        if regex.search(event_id):
            return type

def getEvents(request):
    schedules = {}
    creations = {}
    events = []
    LIMIT = int(request.GET.get('limit'))
    TYPE = request.GET.get('type')
    user_id = request.GET.get('user_id')
    client_instance = Client.objects.get(vk_id_ref=user_id)


    schedulePath = XMLFILES_FOLDER + 'schedules_spb.xml'
    schedulesXML = ET.parse(schedulePath).getroot()
    creationsPath = XMLFILES_FOLDER + 'creations.xml'
    creationsXML = ET.parse(creationsPath).getroot()

    for creationElement in creationsXML:
        creation = Creation()
        if not creationElement.find('main-photo').text:
            del creation
            continue
        creation.creationId = creationElement.find("creation-id").text

        if TYPE and getTypeOfEvent(creation.creationId) != TYPE:
            del creation
            continue
        creation.name = creationElement.find("name").text
        creation.url = creationElement.find("url").text
        creation.description = creationElement.find("description").text
        creation.editorialComment = creationElement.find("editorial-comment").text
        creation.synopsis = creationElement.find("synopsis").text
        creation.image_url = creationElement.find('main-photo').text

        creations[creation.creationId] = creation

    counter = 0
    for scheduleElement in schedulesXML:
        if scheduleElement.find("creation-id").text in creations:
            schedule = Schedule()
            schedule.creationId = scheduleElement.find("creation-id").text
            schedule.begin = scheduleElement.find("begin").text
            schedule.end = scheduleElement.find("end").text
            # schedules[schedule.creationId] = schedule
            counter += 1
            event = Event()
            event.schedule = schedule
            event.creation = creations[schedule.creationId]

            description_ = (event.creation.description) or (event.creation.synopsis) or (event.creation.editorialComment) or ('')
            description_= description_[:100]
            model_event = ModelEvent.objects.get_or_create(
                afisha_event_ref=event.creation.creationId,
                title=event.creation.name[:32],
                description=description_,
                city_id=2,
                start_date=event.schedule.begin,
                end_date=event.schedule.end
            )
            requested_event = ModelEvent.objects.get(afisha_event_ref=event.creation.creationId)
            likes = Likes()
            likes.counter = len(EventUser.objects.filter(event=requested_event))
            likes.user_liked = True if EventUser.objects.filter(event=requested_event, client=client_instance).exists() else False

            event.likes = likes
            events.append(event.createEventDict())
            if counter > LIMIT:
                break
    return JsonResponse(events, safe=False)

def app_index(request):
    user_id = request.GET.get('viewer_id')
    if not Client.objects.filter(vk_id_ref=user_id).exists():
        return redirect('user_info')
    return(render(request, template_name='index.html', using=None))