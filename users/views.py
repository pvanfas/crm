from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_GET
from main.decorators import ajax_required
from main.decorators import check_mode


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
    response_data = {"status": "true", "title": "Success", "message": "User timezone set successfully."}
    return JsonResponse(response_data)
