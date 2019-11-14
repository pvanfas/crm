from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from main.decorators import check_mode, ajax_required
from main.functions import get_auto_id, generate_form_errors, get_a_id
import json
from django.views.decorators.http import require_GET
from users.models import NotificationSubject, Notification
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
import datetime
from calendar import monthrange
from django.utils import timezone
from decimal import Decimal
from products.models import Product
from products.forms import ProductForm
from dal import autocomplete


class ProductAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Product.objects.none()

        items = Product.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(name__icontains=query))

        return items


def get_product(request):
    pk = request.GET.get('id')
    if Product.objects.filter(pk=pk).exists():
        product =  Product.objects.get(pk=pk)

        response_data = {
            "status" : "true",
            "stock" : str(product.stock),
        }
    else:
        response_data = {
            "status" : "false",
            "message" : "Product does not exist."
        }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Product)
            form.save()

            response_data = {
                 "status" : "true",
                 "title" : "Successfully Created",
                 "message" : "Product successfully created",
                 "redirect" : 'true',
                 "redirect_url" : reverse('products:product',kwargs={"pk":data.pk})
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

        form = ProductForm()
        context = {
            "form" : form,
            "title" : "Create product",
            "redirect" : True,

            "is_need_select_picker" : True,
            "is_need_popup_box" : True,
            "is_need_custom_scroll_bar" : True,
            "is_need_wave_effect" : True,
            "is_need_bootstrap_growl" : True,
            "is_need_chosen_select" : True,
            "is_need_grid_system" : True,
            "is_need_datetime_picker" : True,
            "is_need_animations": True,
            "is_dashboard" :True
        }

        return render(request,"products/entry.html", context)


@login_required
def edit(request,pk):
    instance = get_object_or_404(Product.objects.filter(pk=pk))
    if request.method == "POST":
        form = ProductForm(request.POST,instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.updater = request.user
            date_updated = datetime.datetime.now()
            form.save()

            response_data = {
                 "status" : "true",
                 "title" : "Successfully Updated",
                 "message" : "Product successfully Updated",
                 "redirect" : 'true',
                 "redirect_url" : reverse('products:product',kwargs={"pk":data.pk})
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
        form = ProductForm(instance=instance)
        context = {
            "form" : form,
            "title" : "Create Product",
            "redirect" : True,

            "is_need_select_picker" : True,
            "is_need_popup_box" : True,
            "is_need_custom_scroll_bar" : True,
            "is_need_wave_effect" : True,
            "is_need_bootstrap_growl" : True,
            "is_need_chosen_select" : True,
            "is_need_grid_system" : True,
            "is_need_datetime_picker" : True,
            "is_need_animations": True,
            "is_dashboard" :True
        }

        return render(request,"products/entry.html", context)


@login_required
def products(request):
    instances = Product.objects.filter(is_deleted = False)
    context = {
        "title" : "Products",
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

    return render(request, 'products/products.html', context)


@login_required
def product(request,pk):
    instance = get_object_or_404(Product.objects.filter(pk=pk))
    context = {
        "title" : "Product : " + instance.name,
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

    return render(request, 'products/product.html', context)


@login_required
def delete(request,pk):
    Product.objects.filter(pk=pk).update(is_deleted=True)
    response_data = {
         "status" : "true",
         "title" : "Successfully Deleted",
         "message" : "Product successfully Deleted",
         "redirect" : "true",
         "redirect_url" : reverse('products:products')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')
