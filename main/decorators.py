import json

from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseBadRequest
from main.models import Mode


def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def check_mode(function):
    def wrap(request, *args, **kwargs):
        mode, created = Mode.objects.get_or_create()
        readonly = mode.readonly
        down = mode.down

        if down:
            if request.is_ajax():
                response_data = {}
                response_data["status"] = "false"
                response_data[
                    "message"
                ] = "Application currently down. Please try again later."
                response_data["static_message"] = "true"
                return HttpResponse(
                    json.dumps(response_data), content_type="application/javascript"
                )
            else:
                return HttpResponseRedirect(reverse("down"))
        elif readonly:
            if request.is_ajax():
                response_data = {}
                response_data["status"] = "false"
                response_data[
                    "message"
                ] = "Application now readonly mode. please try again later."
                response_data["static_message"] = "true"
                return HttpResponse(
                    json.dumps(response_data), content_type="application/javascript"
                )
            else:
                return HttpResponseRedirect(reverse("read_only"))

        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
