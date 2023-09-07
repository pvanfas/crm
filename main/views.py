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
    context = {"title": "Dashboard", "is_dashboard": True}
    return render(request, "base.html", context)


def down(request):
    context = {}
    return render(request, "main/down.html", context)


def read_only(request):
    context = {}
    return render(request, "main/read_only.html", context)
