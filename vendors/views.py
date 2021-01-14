# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from main.decorators import ajax_required
from main.functions import get_auto_id, generate_form_errors
import json
from django.db.models import Q
import datetime
from vendors.models import Vendor
from vendors.forms import VendorForm


@login_required
def create(request):
    if request.method == "POST":
        form = VendorForm(request.POST,request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Vendor)
            data.save()

            response_data = {
                "status" : "true",
                "title" : "Successfully Created",
                "message" : "Vendor Successfully Created.",
                "redirect" : "true",
                "redirect_url" : reverse('vendors:vendor',kwargs={"pk":data.pk})
            }
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = VendorForm()
        context = {
            "form" : form,
            "title" : "Create Vendor",
            "redirect" : True,
            "url" : reverse('vendors:create'),

            "is_need_select_picker" : True,
            "is_need_popup_box" : True,
            "is_need_custom_scroll_bar" : True,
            "is_need_wave_effect" : True,
            "is_need_bootstrap_growl" : True,
            "is_need_chosen_select" : True,
            "is_need_grid_system" : True,
            "is_need_datetime_picker" : True,
            "is_need_animations": True,
        }

        return render(request,'vendors/entry.html',context)


@login_required
def edit(request,pk):
    if request.method == "POST":
        instance = get_object_or_404(Vendor.objects.filter(pk=pk))
        form = VendorForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()

            response_data = {
                "status" : "true",
                "title" : "Successfully Updated",
                "message" : "Vendor Successfully Updated.",
                "redirect" : "true",
                "redirect_url" : reverse('vendors:vendor',kwargs={"pk":data.pk})
            }
        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        instance = get_object_or_404(Vendor.objects.filter(pk=pk))
        form = VendorForm(instance=instance)
        context = {
            "form" : form,
            "title" : "Edit Vendor",
            "redirect" : True,
            "url" : reverse('vendors:edit',kwargs={"pk":instance.pk}),

            "is_need_select_picker" : True,
            "is_need_popup_box" : True,
            "is_need_custom_scroll_bar" : True,
            "is_need_wave_effect" : True,
            "is_need_bootstrap_growl" : True,
            "is_need_chosen_select" : True,
            "is_need_grid_system" : True,
            "is_need_datetime_picker" : True,
            "is_need_animations": True,
        }

        return render(request,'vendors/entry.html',context)


@login_required
def vendor(request,pk):
    instance = get_object_or_404(Vendor.objects.filter(pk=pk))
    context = {
        "title" : "Vendor : " + instance.name,
        "instance" : instance,

        "is_need_select_picker" : True,
        "is_need_popup_box" : True,
        "is_need_custom_scroll_bar" : True,
        "is_need_wave_effect" : True,
        "is_need_bootstrap_growl" : True,
        "is_need_chosen_select" : True,
        "is_need_grid_system" : True,
        "is_need_datetime_picker" : True,
        "is_need_animations": True,
    }
    return render(request,'vendors/vendor.html',context)


@login_required
def vendors(request):
    instances = Vendor.objects.filter(is_deleted=False)

    query = request.GET.get('q')
    if query:
        instances = instances.filter(Q(name__icontains=query) | Q(phone__icontains=query) | Q(email__icontains=query) | Q(address__icontains=query))
    context = {
        "title" : "Vendors",
        "instances" : instances,

        "is_need_select_picker" : True,
        "is_need_popup_box" : True,
        "is_need_custom_scroll_bar" : True,
        "is_need_wave_effect" : True,
        "is_need_bootstrap_growl" : True,
        "is_need_chosen_select" : True,
        "is_need_grid_system" : True,
        "is_need_datetime_picker" : True,
        "is_need_animations": True,
    }
    return render(request,'vendors/vendors.html',context)


@login_required
@ajax_required
def delete(request,pk):
    Vendor.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status" : "true",
        "title" : "Vendor Deleted",
        "message" : "Vendor Successfully Deleted.",
        "redirect" : "true",
        "redirect_url" : reverse('vendors:vendors')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')

@login_required
def get_vendor(request):
    pk = request.GET.get('id')
    if Vendor.objects.filter(pk=pk).exists():
        vendor = Vendor.objects.get(pk=pk)

        response_data = {
            "status" : "true",
            "name" : vendor.name,
            "phone" : vendor.phone,
            "email" : vendor.email,
            "address" : vendor.address,
            "pk" : str(vendor.pk)
        }
    else:
        response_data = {
            "status" : "false",
            "message" : "Vendor not exists."
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def delete_selected_vendor(request):
    pks = request.GET.get('pk')
    print(pks)
    if pks:
        pks = pks[:-1]

        pks = pks.split(',')
        for pk in pks:
            instance = get_object_or_404(Vendor.objects.filter(pk=pk,is_deleted=False))
            instance.is_deleted = True
            instance.save()

        response_data = {
            "status" : "true",
            "title" : "Successfully Deleted",
            "message" : "Selected Sale(s) Successfully Deleted.",

        }
    else:
        response_data = {
            "status" : "false",
            "title" : "Nothing selected",
            "message" : "Please select some items first.",
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')
