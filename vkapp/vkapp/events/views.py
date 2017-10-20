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
        return dict

    def __eq__(self, other):
        return self.creation.creationId == other.creation.creationId

    def __hash__(self):
        return hash(('creationId', self.creation.creationId))

def getEvents(request):
    schedules = {}
    creations = {}
    events = []

    schedulePath = XMLFILES_FOLDER + 'schedules_spb.xml'
    schedulesXML = ET.parse(schedulePath).getroot()
    creationsPath = XMLFILES_FOLDER + 'creations.xml'
    creationsXML = ET.parse(creationsPath).getroot()

    for creationElement in creationsXML:
        creation = Creation()
        creation.creationId = creationElement.find("creation-id").text
        creation.name = creationElement.find("name").text
        creation.url = creationElement.find("url").text
        creation.description = creationElement.find("description").text
        creation.editorialComment = creationElement.find("editorial-comment").text
        creation.synopsis = creationElement.find("synopsis").text

        creations[creation.creationId] = creation

    for scheduleElement in schedulesXML:
        schedule = Schedule()
        schedule.creationId = scheduleElement.find("creation-id").text
        schedule.begin = scheduleElement.find("begin").text
        schedule.end = scheduleElement.find("end").text
        schedules[schedule.creationId] = schedule

    # schedules = set(schedules)

    for key, value in schedules.items():
        event = Event()
        event.schedule = value
        event.creation = creations[key]
        events.append(event.createEventDict())

    return JsonResponse(events, safe=False)