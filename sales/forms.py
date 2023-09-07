from django import forms
from django.forms.widgets import Select
from django.forms.widgets import TextInput
from django.utils.translation import gettext_lazy as _
from sales.models import Sale
from sales.models import SaleItem


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        exclude = ["creator", "updater", "auto_id", "is_deleted", "total", "sub_total"]
        widgets = {
            "customer": Select(attrs={"class": "required form-control", "data-placeholder": "Customer"}),
            "date": TextInput(attrs={"class": "required form-control date-picker", "placeholder": "Date"}),
            "discount": TextInput(attrs={"class": "required number form-control", "placeholder": "Discount"}),
        }
        error_messages = {
            "customer": {"required": _("Customer field is required.")},
            "date": {"required": _("Date field is required.")},
            "discount": {"required": _("Discount field is required.")},
        }


class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        exclude = ["sale"]
        widgets = {
            "product": Select(attrs={"class": "required form-control", "data-placeholder": "Product"}),
            "qty": TextInput(attrs={"class": "required number form-control", "placeholder": "Qty"}),
        }
        error_messages = {
            "product": {"required": _("Product field is required.")},
            "qty": {"required": _("Qauntity field is required.")},
        }
