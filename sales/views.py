import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.forms.widgets import Select
from django.forms.widgets import TextInput
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from main.decorators import ajax_required
from main.functions import generate_form_errors
from main.functions import get_auto_id
from products.models import Product
from sales.forms import SaleForm
from sales.forms import SaleItemForm
from sales.functions import update_stock
from sales.models import Sale
from sales.models import SaleItem


@login_required
def create(request):
    SaleItemFormset = formset_factory(SaleItemForm, extra=1)
    if request.method == "POST":
        form = SaleForm(request.POST)
        sale_item_formset = SaleItemFormset(request.POST, prefix="sale_item_formset")
        if form.is_valid() and sale_item_formset.is_valid():
            # Creating Sale Item Objects for finding duplicate product entry
            items = {}
            for f in sale_item_formset:
                product = f.cleaned_data["product"]
                qty = f.cleaned_data["qty"]
                if str(product.pk) in items:
                    q = items[str(product.pk)]["qty"]
                    items[str(product.pk)]["qty"] = q + qty
                else:
                    dic = {"qty": qty}
                    items[str(product.pk)] = dic

            # Checking the stock available for this product
            stock_ok = True
            error_message = ""
            for key, value in items.items():
                product = Product.objects.get(pk=key)
                stock = product.stock
                qty = value["qty"]
                if qty > stock:
                    stock_ok = False
                    error_message += "%s has only %s in stock, You entered %s qty" % (
                        product.name,
                        str(stock),
                        str(qty),
                    )

            if stock_ok:
                discount = form.cleaned_data["discount"]

                data = form.save(commit=False)
                data.creator = request.user
                data.updater = request.user
                data.auto_id = get_auto_id(Sale)
                data.save()

                sub_total = 0
                for key, value in items.items():
                    product = Product.objects.get(pk=key)
                    qty = value["qty"]
                    price = product.price
                    sub = qty * price
                    sub_total += sub

                    SaleItem(product=product, qty=qty, sale=data).save()

                    update_stock(product.pk, qty, "decrease")

                total = sub_total - discount

                data.sub_total = sub_total
                data.total = total
                data.save()

                response_data = {
                    "status": "true",
                    "title": "Successfully Created",
                    "message": "Sale Successfully Created.",
                    "redirect": "true",
                    "redirect_url": reverse("sales:sale", kwargs={"pk": data.pk}),
                }
            else:
                response_data = {"status": "false", "stable": "true", "title": "Out of Stock", "message": error_message}
        else:
            message = generate_form_errors(form, formset=False)
            message += generate_form_errors(sale_item_formset, formset=True)
            response_data = {"status": "false", "stable": "true", "title": "Form validation error", "message": message}

        return JsonResponse(response_data)
    else:
        form = SaleForm()
        sale_item_formset = SaleItemFormset(prefix="sale_item_formset")
        context = {
            "form": form,
            "sale_item_formset": sale_item_formset,
            "title": "Create Sale",
            "redirect": True,
            "url": reverse("sales:create"),
            "is_create_page": True,
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

        return render(request, "sales/entry.html", context)


@login_required
def edit(request, pk):
    instance = get_object_or_404(Sale.objects.filter(pk=pk, is_deleted=False))

    if SaleItem.objects.filter(sale=instance).exists():
        extra = 0
    else:
        extra = 1

    SaleItemFormset = inlineformset_factory(
        Sale,
        SaleItem,
        can_delete=True,
        extra=extra,
        exclude=["creator", "updater", "auto_id", "is_deleted", "sale"],
        widgets={
            "product": Select(attrs={"class": "required form-control", "data-placeholder": "Product"}),
            "qty": TextInput(attrs={"class": "required number form-control", "placeholder": "Quantity"}),
        },
    )
    if request.method == "POST":
        form = SaleForm(request.POST, instance=instance)
        sale_item_formset = SaleItemFormset(request.POST, prefix="sale_item_formset", instance=instance)

        if form.is_valid() and sale_item_formset.is_valid():
            items = {}
            for f in sale_item_formset:
                if f not in sale_item_formset.deleted_forms:
                    product = f.cleaned_data["product"]
                    qty = f.cleaned_data["qty"]
                    if str(product.pk) in items:
                        q = items[str(product.pk)]["qty"]
                        items[str(product.pk)]["qty"] = q + qty

                    else:
                        dic = {"qty": qty}
                        items[str(product.pk)] = dic

            stock_ok = True
            error_message = ""
            for key, value in items.items():
                product = Product.objects.get(pk=key)
                prev_qty = 0
                if SaleItem.objects.filter(sale=instance, product=product).exists():
                    prev_qty = SaleItem.objects.get(sale=instance, product=product).qty
                stock = product.stock + prev_qty

                product_qty = value["qty"]
                if product_qty > stock:
                    stock_ok = False
                    error_message += "%s has only %s in stock, You entered %s qty" % (
                        product.name,
                        str(stock),
                        str(qty),
                    )

            stock_ok = True
            error_message = ""
            for key, value in items.items():
                product = Product.objects.get(pk=key)
                prev_qty = 0
                if SaleItem.objects.filter(sale=instance, product=product).exists():
                    prev_qty = SaleItem.objects.get(sale=instance, product=product).qty
                stock = product.stock + prev_qty

                product_qty = value["qty"]
                if product_qty > stock:
                    stock_ok = False
                    error_message += "%s has only %s in stock, " % (product.name, str(stock))

            if stock_ok:
                # update sale
                discount = form.cleaned_data["discount"]

                data = form.save(commit=False)
                data.updator = request.user
                data.date_updated = datetime.datetime.now()
                data.save()

                all_subtotal = 0

                # delete previous items and update stock
                previous_sale_items = SaleItem.objects.filter(sale=instance)
                for p in previous_sale_items:
                    prev_qty = p.qty
                    update_stock(p.product.pk, prev_qty, "increase")
                previous_sale_items.delete()

                # save items
                for key, value in items.items():
                    product = Product.objects.get(pk=key)
                    qty = value["qty"]
                    price = product.price
                    sub_total = qty * price
                    all_subtotal += sub_total
                    SaleItem(sale=data, product=product, qty=qty).save()

                    update_stock(product.pk, qty, "decrease")

                total = all_subtotal - discount

                data.sub_total = all_subtotal
                data.total = total
                data.save()

                response_data = {
                    "status": "true",
                    "title": "Successfully Updated",
                    "message": "Sale Successfully Updated.",
                    "redirect": "true",
                    "redirect_url": reverse("sales:sale", kwargs={"pk": data.pk}),
                }
            else:
                response_data = {"status": "false", "stable": "true", "title": "Out of Stock", "message": error_message}
        else:
            message = generate_form_errors(form, formset=False)
            message += generate_form_errors(sale_item_formset, formset=True)
            response_data = {"status": "false", "stable": "true", "title": "Form validation error", "message": message}

        return JsonResponse(response_data)
    else:
        form = SaleForm(instance=instance)
        sale_item_formset = SaleItemFormset(prefix="sale_item_formset", instance=instance)
        context = {
            "form": form,
            "title": "Edit Sale #: " + str(instance.auto_id),
            "instance": instance,
            "sale_item_formset": sale_item_formset,
            "redirect": True,
            "url": reverse("sales:edit", kwargs={"pk": instance.pk}),
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

        return render(request, "sales/entry.html", context)


@login_required
def sale(request, pk):
    instance = get_object_or_404(Sale.objects.filter(pk=pk))
    sale_items = SaleItem.objects.filter(sale=instance)
    context = {
        "title": "Sale : " + str(instance.auto_id),
        "instance": instance,
        "sale_items": sale_items,
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
    return render(request, "sales/sale.html", context)


@login_required
def sales(request):
    instances = Sale.objects.filter(is_deleted=False)
    query = request.GET.get("q")
    if query:
        instances = instances.filter(
            Q(customer__name__icontains=query)
            | Q(customer__phone__icontains=query)
            | Q(customer__email__icontains=query)
            | Q(customer__address__icontains=query)
        )

    context = {
        "title": "Sales",
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
    return render(request, "sales/sales.html", context)


@login_required
@ajax_required
def delete(request, pk):
    instance = get_object_or_404(Sale.objects.filter(pk=pk))

    # update stock
    sale_items = SaleItem.objects.filter(sale=instance)
    for p in sale_items:
        qty = p.qty
        update_stock(p.product.pk, qty, "increase")

    instance.is_deleted = True
    instance.save()

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Sale Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse("sales:sales"),
    }
    return JsonResponse(response_data)


@login_required
def delete_selected_sale(request):
    pks = request.GET.get("pk")
    print(pks)
    if pks:
        pks = pks[:-1]

        pks = pks.split(",")
        for pk in pks:
            instance = get_object_or_404(Sale.objects.filter(pk=pk, is_deleted=False))
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
