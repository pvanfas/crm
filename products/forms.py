from django import forms
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _
from products.models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ['creator','updater','auto_id','is_deleted']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Name'}),
            'cost': TextInput(attrs={'class': 'required form-control ','placeholder' : 'Cost'}),
            'stock': TextInput(attrs={'class': 'required form-control','placeholder' : 'Stoke'}),
            'price': TextInput(attrs={'class': 'required form-control','placeholder' : 'Price'}),
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
            'stoke' : {
                'required' : _("Stoke field is required."),
            },
        }
