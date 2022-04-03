import json

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_GET

from main.decorators import ajax_required, check_mode


@check_mode
@login_required
def dashboard(request):
    return HttpResponseRedirect(reverse("app"))


@login_required
@ajax_required
@require_GET
def set_user_timezone(request):
    timezone = request.GET.get("timezone")
    request.session["set_user_timezone"] = timezone
    response_data = {}
    response_data["status"] = "true"
    response_data["title"] = "Success"
    response_data["message"] = "user timezone set successfully."
    return HttpResponse(
        json.dumps(response_data), content_type="application/javascript"
    )
