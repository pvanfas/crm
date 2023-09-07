from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
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
        readonly, down = mode.readonly, mode.down

        if down:
            message = "Application currently down. Please try again later."
            return _handle_mode(request, message, is_ajax=request.is_ajax(), is_static_message=True)

        if readonly:
            message = "Application now in readonly mode. Please try again later."
            return _handle_mode(request, message, is_ajax=request.is_ajax(), is_static_message=True)

        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def _handle_mode(request, message, is_ajax=False, is_static_message=False):
    if is_ajax:
        response_data = {
            "status": "false",
            "message": message,
            "static_message": "true" if is_static_message else "false",
        }
        return JsonResponse(response_data)
    else:
        return HttpResponseRedirect(reverse("down") if is_static_message else reverse("read_only"))
