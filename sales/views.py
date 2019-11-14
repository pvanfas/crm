from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from main.decorators import check_mode, ajax_required
from main.functions import get_auto_id, generate_form_errors, get_a_id
import json
from django.views.decorators.http import require_GET
from users.models import NotificationSubject, Notification
from django.db.models import Sum, Q
from django.contrib.auth.models import Group
import datetime
from django.utils import timezone
from decimal import Decimal
from sales.models import Sale, SaleItem
from sales.forms import SaleForm, SaleItemForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import TextInput,Select
from django.forms.formsets import formset_factory
from products.models import Product
from customers.models import Customer
from products.functions import update_stock
from dal import autocomplete


class CustomerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Customer.objects.none()

        items = Customer.objects.filter(is_deleted=False)

        if self.q:
            query = self.q
            items = items.filter(Q(name__icontains=query) | Q(phone__icontains=query) | Q(email__icontains=query) | Q(address__icontains=query))
        return items


@login_required
def create(request):
    SaleItemFormset = formset_factory(SaleItemForm,extra=1)

    if request.method == 'POST':
        form = SaleForm(request.POST)
        sale_item_formset = SaleItemFormset(request.POST,prefix="sale_item_formset")
        if form.is_valid() and sale_item_formset.is_valid():

            # Creating Sale Item Objects for finding duplicate product entry
            items = {}
            for f in sale_item_formset:
                product = f.cleaned_data['product']
                qty = f.cleaned_data['qty']
                if str(product.pk) in items:
                    q = items[str(product.pk)]["qty"]
                    items[str(product.pk)]["qty"] = q + qty
                else:
                    dic = {
                        "qty" : qty,
                    }
                    items[str(product.pk)] = dic

            # Checking the stock available for this product
            stock_ok = True
            error_message = ''
            for key, value in items.iteritems():
                product = Product.objects.get(pk=key)
                stock = product.stock
                qty = value['qty']
                if qty > stock:
                    stock_ok = False
                    error_message += "%s has only %s in stock, You entered %s qty" %(product.name,str(stock),str(qty))

            if stock_ok:
                discount = form.cleaned_data['discount']

                data = form.save(commit=False)
                data.creator = request.user
                data.updater = request.user
                data.auto_id = get_auto_id(Sale)
                data.save()

                subtotal = 0
                for key, value in items.iteritems():
                    product = Product.objects.get(pk=key)
                    qty = value["qty"]
                    price = product.price
                    sub = (qty * price)
                    subtotal += sub

                    SaleItem(
                        sale = data,
                        product = product,
                        qty = qty
                    ).save()

                    update_stock(product.pk,qty,"decrease")

                total = subtotal - discount

                data.subtotal = subtotal
                data.total = total
                data.save()

                response_data = {
                    "status" : "true",
                    "title" : "Successfully Created",
                    "message" : "Sale Successfully Created.",
                    "redirect" : "true",
                    "redirect_url" : reverse('sales:sale',kwargs={'pk':data.pk})
                }
            else:
                response_data = {
                    "status" : "false",
                    "stable" : "true",
                    "title" : "Out of Stock",
                    "message" : error_message
                }
        else:
            message = generate_form_errors(form,formset=False)
            message += generate_form_errors(sale_item_formset,formset=True)
            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = SaleForm()
        sale_item_formset = SaleItemFormset(prefix="sale_item_formset")
        context = {
            "title" : "Create Sale",
            "form" : form,
            "sale_item_formset" : sale_item_formset,
            "url" : reverse('sales:create'),
            "redirect" : True,
            "is_create_page" : True,

            "is_need_select_picker" : True,
            "is_need_popup_box" : True,
            "is_need_custom_scroll_bar" : True,
            "is_need_wave_effect" : True,
            "is_need_bootstrap_growl" : True,
            "is_need_chosen_select" : True,
            "is_need_grid_system" : True,
            "is_need_datetime_picker" : True,
        }
        return render(request,'sales/entry.html',context)


@login_required
def edit(request,pk):
    instance = get_object_or_404(Sale.objects.filter(pk=pk,is_deleted=False))

    if SaleItem.objects.filter(sale=instance).exists():
        extra = 0
    else:
        extra= 1

    SaleItemFormset = inlineformset_factory(
        Sale,
        SaleItem,
        can_delete = True,
        extra = extra,
        exclude=('sale',),
        widgets = {
            'product': autocomplete.ModelSelect2(url='products:product_autocomplete',attrs={'data-placeholder': 'Product','data-minimum-input-length': 1},),
            'qty': TextInput(attrs={'class': 'required number form-control','placeholder' : 'Quantity'}),
        }
    )

    if request.method == 'POST':
        form = SaleForm(request.POST,instance=instance)
        sale_item_formset = SaleItemFormset(request.POST,prefix='sale_item_formset',instance=instance)

        if form.is_valid() and sale_item_formset.is_valid():

            items = {}

            for f in sale_item_formset:
                if f not in sale_item_formset.deleted_forms:
                    product = f.cleaned_data['product']
                    qty = f.cleaned_data['qty']
                    if str(product.pk) in items:
                        q = items[str(product.pk)]["qty"]
                        items[str(product.pk)]["qty"] = q + qty

                    else:
                        dic = {
                            "qty" : qty
                        }
                        items[str(product.pk)] = dic

            stock_ok = True
            error_message = ''
            for key, value in items.iteritems():
                product = Product.objects.get(pk=key)
                prev_qty = 0
                if SaleItem.objects.filter(sale=instance,product=product).exists():
                    prev_qty = SaleItem.objects.get(sale=instance,product=product).qty
                stock = product.stock + prev_qty

                product_qty = value['qty']
                if product_qty > stock:
                    stock_ok = False
                    error_message += "%s has only %s in stock, " %(product.name,str(stock))

            if stock_ok:

                #update sale
                discount = form.cleaned_data['discount']

                data = form.save(commit=False)
                data.updator = request.user
                data.date_updated = datetime.datetime.now()
                data.save()

                all_subtotal = 0

                #delete previous items and update stock
                previous_sale_items = SaleItem.objects.filter(sale=instance)
                for p in previous_sale_items:
                    prev_qty = p.qty
                    update_stock(p.product.pk,prev_qty,"increase")
                previous_sale_items.delete()

                #save items
                for key, value in items.iteritems():
                    product = Product.objects.get(pk=key)
                    qty = value["qty"]
                    price = product.price
                    subtotal = (qty * price)
                    all_subtotal += subtotal
                    SaleItem(
                        sale = data,
                        product = product,
                        qty = qty,
                    ).save()

                    update_stock(product.pk,qty,"decrease")

                total = all_subtotal - discount

                data.subtotal = all_subtotal
                data.total = total
                data.save()

                response_data = {
                    "status" : "true",
                    "title" : "Successfully Updated",
                    "message" : "Sale Successfully Updated.",
                    "redirect" : "true",
                    "redirect_url" : reverse('sales:sale',kwargs={'pk':data.pk})
                }
            else:
                response_data = {
                    "status" : "false",
                    "stable" : "true",
                    "title" : "Out of Stock",
                    "message" : error_message
                }
        else:
            print("Error")
            message = generate_form_errors(form,formset=False)
            message += generate_form_errors(sale_item_formset,formset=True)
            response_data = {
                "status" : "false",
                "stable" : "true",
                "title" : "Form validation error",
                "message" : message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = SaleForm(instance=instance)
        sale_item_formset = SaleItemFormset(prefix="sale_item_formset",instance=instance)
        context = {
            "form" : form,
            "title" : "Edit Sale #: " + str(instance.auto_id),
            'instance': instance,
            "url" : reverse('sales:edit',kwargs={'pk':instance.pk}),
            "sale_item_formset" : sale_item_formset,
            "redirect" : True,

            "is_need_select_picker" : True,
            "is_need_popup_box" : True,
            "is_need_custom_scroll_bar" : True,
            "is_need_wave_effect" : True,
            "is_need_bootstrap_growl" : True,
            "is_need_chosen_select" : True,
            "is_need_grid_system" : True,
            "is_need_datetime_picker" : True,
        }
    return render(request,'sales/entry.html',context)


@login_required
def sales(request):
    instances = Sale.objects.filter(is_deleted = False)
    query = request.GET.get('q')

    if query:
        instances = instances.filter(Q(customer__name__icontains=query) | Q(customer__phone__icontains=query) | Q(customer__email__icontains=query) | Q(customer__address__icontains=query))

    context = {
        "title" : "Sales",
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

    return render(request, 'sales/sales.html', context)


@login_required
def sale(request,pk):
    instance = get_object_or_404(Sale.objects.filter(pk=pk))
    sale_items = SaleItem.objects.filter(sale=instance)
    context = {
        "title" : "sale: " + str(instance.auto_id),
        "instance" : instance,
        "sale_items" : sale_items,

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

    return render(request, 'sales/sale.html', context)


@login_required
def delete(request,pk):
    instance = get_object_or_404(Sale.objects.filter(pk=pk))

    #update stock
    sale_items =SaleItem.objects.filter(sale=instance)
    for product in sale_items:
        qty = product.qty
        update_stock(product.product.pk,qty,"increase")

        instance.is_deleted = True
        instance.save()

    response_data = {
         "status" : "true",
         "title" : "Successfully Deleted",
         "message" : "Sale successfully Deleted",
         "redirect" : "true",
         "redirect_url" : reverse('sales:sales')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')
