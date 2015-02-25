from django.shortcuts import render_to_response
from django.http import Http404
from django.conf import settings
from djenealogy import models


def index(request):
    data = {
        'STATIC_URL': settings.STATIC_URL,
        'MEDIA_URL': settings.MEDIA_URL,
        'DEBUG': settings.DEBUG
    }
    
    return render_to_response('djenealogy/app.html', data)
