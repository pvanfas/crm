import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from main.decorators import ajax_required
from main.functions import generate_form_errors
from main.functions import get_auto_id
from products.forms import ProductForm
from products.models import Product


@login_required
def create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Product)
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Product Successfully Created.",
                "redirect": "true",
                "redirect_url": reverse("products:product", kwargs={"pk": data.pk}),
            }
        else:
            message = generate_form_errors(form, formset=False)

            response_data = {"status": "false", "stable": "true", "title": "Form validation error", "message": message}

        return JsonResponse(response_data)
    else:
        form = ProductForm()
        context = {
            "form": form,
            "title": "Create Product",
            "redirect": True,
            "url": reverse("products:create"),
            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, "products/entry.html", context)


@login_required
def edit(request, pk):
    if request.method == "POST":
        instance = get_object_or_404(Product.objects.filter(pk=pk))
        form = ProductForm(request.POST, instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.now()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Product Successfully Updated.",
                "redirect": "true",
                "redirect_url": reverse("products:product", kwargs={"pk": data.pk}),
            }
        else:
            message = generate_form_errors(form, formset=False)

            response_data = {"status": "false", "stable": "true", "title": "Form validation error", "message": message}

        return JsonResponse(response_data)
    else:
        instance = get_object_or_404(Product.objects.filter(pk=pk))
        form = ProductForm(instance=instance)
        context = {
            "form": form,
            "title": "Edit Product",
            "redirect": True,
            "url": reverse("products:edit", kwargs={"pk": instance.pk}),
            "is_need_select_picker": True,
            "is_need_popup_box": True,
            "is_need_custom_scroll_bar": True,
            "is_need_wave_effect": True,
            "is_need_bootstrap_growl": True,
            "is_need_chosen_select": True,
            "is_need_grid_system": True,
            "is_need_datetime_picker": True,
            "is_need_animations": True,
        }

        return render(request, "products/entry.html", context)


@login_required
def product(request, pk):
    instance = get_object_or_404(Product.objects.filter(pk=pk))
    context = {
        "title": "Product : " + instance.name,
        "instance": instance,
        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }
    return render(request, "products/product.html", context)


@login_required
def products(request):
    instances = Product.objects.filter(is_deleted=False)
    query = request.GET.get("q")
    if query:
        instances = instances.filter(
            Q(name__icontains=query) | Q(cost__contains=query) | Q(price__contains=query) | Q(stock__contains=query)
        )
    context = {
        "title": "Products",
        "instances": instances,
        "is_need_select_picker": True,
        "is_need_popup_box": True,
        "is_need_custom_scroll_bar": True,
        "is_need_wave_effect": True,
        "is_need_bootstrap_growl": True,
        "is_need_chosen_select": True,
        "is_need_grid_system": True,
        "is_need_datetime_picker": True,
        "is_need_animations": True,
    }
    return render(request, "products/products.html", context)


@login_required
@ajax_required
def delete(request, pk):
    Product.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Product Deleted",
        "message": "Product Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse("products:products"),
    }
    return JsonResponse(response_data)


@login_required
@ajax_required
def get_product(request):
    pk = request.GET.get("id")
    if Product.objects.filter(pk=pk).exists():
        product = Product.objects.get(pk=pk)

        response_data = {"status": "true", "stock": str(product.stock)}
    else:
        response_data = {"status": "false", "message": "Product not exists."}

    return JsonResponse(response_data)


@login_required
def delete_selected_products(request):
    pks = request.GET.get("pk")
    print(pks)
    if pks:
        pks = pks[:-1]

        pks = pks.split(",")
        for pk in pks:
            instance = get_object_or_404(Product.objects.filter(pk=pk, is_deleted=False))
            instance.is_deleted = True
            instance.save()

        response_data = {
            "status": "true",
            "title": "Successfully Deleted",
            "message": "Selected Sale(s) Successfully Deleted.",
        }
    else:
        response_data = {"status": "false", "title": "Nothing selected", "message": "Please select some items first."}

    return JsonResponse(response_data)
