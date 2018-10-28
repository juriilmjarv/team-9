import json
from urllib.request import urlopen
#from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
#from codeforgood.models import Users, Locations, Tags, Location_Tags, Favourites, Saved_Searches
#from django.contrib.auth import authenticate, login
#from django.core.urlresolvers import reverse
#from django.shortcuts import render
#from social.forms import RegistrationForm, UserProfileForm
from django.shortcuts import render
from codeforgood.models import Locations
from django.http import HttpRequest
from django.http import HttpResponse
import datetime
#from django.core.urlresolvers import reverse
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth import logout
# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from math import sin, cos, sqrt, atan2, radians
# import re
# approximate radius of earth in km


def getLocation():


    url = 'http://ipinfo.io?token=b4c8c534242400'
    response =urlopen(url)
    data = json.load(response)
    loc = data['loc']
    return loc

def calculateDistance():
    location = getLocation().split(',')
    R = 6373.0

    lat1 = radians(float(location[0]))
    lon1 = radians(float(location[1]))
    lat2 = radians(56)
    lon2 = radians(-4)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    print("Result:", distance)


def index(request):
    return render(request, 'index.html')

def search(request):
    input = request.GET.get('name','')
    good_input = input.split()
    tags = Tags.objects.all()
    tags_location = Location_Tags.objects.all()               #
    tags_list = []
    tags_final = []
    locations = Locations.objects.all()
    results = []
    if (good_input[0] != ""):
        for input in good_input:
            for tag in tags:
                if( input == tag):
                    tags_list.append(tag)
        for tag in tags_list:
            for tag_loc in  tags_location:
                if(tag == tag_loc.tag):
                    tags_final.append(tag_loc)
        for location in locations:
            islocation = False
            for input in good_input:
                if(location.name.find(input) != -1):
                    results.append(location)
                    islocation = True
                    break
            if(not islocation):
                valid = False
                for tag in tags_final:
                    if(tag.location == location.id):
                        results.append(location)
                        valid = True
                        break
                if(not valid):
                    for input in good_input:
                        if(location.description.find(input) != -1):
                            results.append(location)
                            break;

        print(results)
    else:
        return locations

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codeforgood.settings')
import django
django.setup()
from codeforgood.models import Locations, Tags, Location_Tags