from django.shortcuts import render
from main.models import Mode
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json


def ajax_required(function):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return render(request,'error/400.html',{})
        return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap


def check_mode(function):
    def wrap(request, *args, **kwargs):
        mode = Mode.objects.get(id=1)
        readonly = mode.readonly
        maintenance = mode.maintenance
        down = mode.down

        if down:
            if request.is_ajax():
                response_data = {}
                response_data['status'] = 'false'
                response_data['message'] = "Application currently down. Please try again later."
                response_data['static_message'] = "true"
                return HttpResponse(json.dumps(response_data), content_type='application/javascript')
            else:
                return HttpResponseRedirect(reverse('down'))
        elif readonly:
            if request.is_ajax():
                response_data = {}
                response_data['status'] = 'false'
                response_data['message'] = "Application now readonly mode. please try again later."
                response_data['static_message'] = "true"
                return HttpResponse(json.dumps(response_data), content_type='application/javascript')
            else:
                return HttpResponseRedirect(reverse('read_only'))

        return function(request, *args, **kwargs)

    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap