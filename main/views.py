from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from main.decorators import check_mode


@check_mode
@login_required
def app(request):
    return HttpResponseRedirect(reverse("dashboard"))


@check_mode
@login_required
def dashboard(request):
    context = {
        "title": "Dashboard",
        "is_dashboard": True,
        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
        "is_dashboard": True,
    }
    return render(request, "base.html", context)
