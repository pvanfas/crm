from django import forms
from django.forms.widgets import TextInput, Textarea, Select
from django.utils.translation import ugettext_lazy as _
from sales.models import Sale, SaleItem
from dal import autocomplete

class SaleForm(forms.ModelForm):

    class Meta:
        model = Sale
        exclude = ['creator','updater','auto_id','is_deleted','total','sub_total']
        widgets = {
            'customer': autocomplete.ModelSelect2(url='customers:customer_autocomplete',attrs={'data-placeholder': 'Customer','data-minimum-input-length': 1},),
            'date': TextInput(attrs={'class': 'required form-control date-picker','placeholder' : 'Date'}),
            'discount': TextInput(attrs={'class': 'required number form-control','placeholder' : 'Discount'}),
        }
        error_messages = {
            'customer' : {
                'required' : _("Customer field is required."),
            },
            'date' : {
                'required' : _("Date field is required."),
            },
            'discount' : {
                'required' : _("Discount field is required."),
            },
        }


class SaleItemForm(forms.ModelForm):

    class Meta:
        model = SaleItem
        exclude = ['sale']
        widgets = {
            'product' : autocomplete.ModelSelect2(url='products:product_autocomplete',attrs={'data-placeholder': 'Product','data-minimum-input-length': 0},),
            'qty': TextInput(attrs={'class': 'required number form-control','placeholder' : 'Qty'}),
        }
        error_messages = {
            'product' : {
                'required' : _("Product field is required."),
            },
            'qty' : {
                'required' : _("Qauntity field is required."),
            },
        }
