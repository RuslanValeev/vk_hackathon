from django.shortcuts import render

# Create your views here.

import xml.etree.ElementTree as ET
from django.http import JsonResponse
from vkapp.settings import XMLFILES_FOLDER
import json

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

class Event:
    creation = Creation()
    schedule = Schedule()

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
        return dict

    def __eq__(self, other):
        return self.creation.creationId == other.creation.creationId

    def __hash__(self):
        return hash(('creationId', self.creation.creationId))

def getEvents(request):
    schedules = {}
    creations = {}
    events = []
    LIMIT = int(request.GET.get('limit'))

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
            events.append(event.createEventDict())
            if counter > LIMIT:
                break
    return JsonResponse(events, safe=False)

def app_index(request):
    return(render(request, template_name='index.html', using=None))