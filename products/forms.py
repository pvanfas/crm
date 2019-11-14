from django import forms
from django.forms.widgets import TextInput, Textarea, Select
from django.utils.translation import ugettext_lazy as _
from products.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['auto_id','creator','updater','is_deleted']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Name'}),
            'cost': TextInput(attrs={'class': 'required form-control','placeholder' : 'Cost'}),
            'price': TextInput(attrs={'class': 'required form-control','placeholder' : 'Price'}),
            'stock': TextInput(attrs={'class': 'required form-control','placeholder' : 'Stock'}),
        }
        error_messages = {
            'name' : {
                'required' : _("Name field is required."),
            },
            'cost' : {
                'required' : _("Cost field is required."),
            },
            'price' : {
                'required' : _("Price field is required."),
            },
            'stock' : {
                'required' : _("Stock field is required."),
            },
        }