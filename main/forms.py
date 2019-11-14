from django import forms
from django.forms.widgets import TextInput, Textarea, Select
from django.utils.translation import ugettext_lazy as _
from main.models import Shop


class ShopForm(forms.ModelForm):

    class Meta:
        model = Shop
        exclude = ['creator','updator','auto_id','is_deleted']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Name'}),
            'email': TextInput(attrs={'class': 'required form-control','placeholder' : 'Email'}),
            'phone': TextInput(attrs={'class': 'required form-control','placeholder' : 'Phone'}),
            'address': TextInput(attrs={'class': 'required form-control','placeholder' : 'Address'}),
            'website': TextInput(attrs={'class': 'form-control','placeholder' : 'Website'}),
            'theme': Select(attrs={'class': 'required selectpicker'}),
            'state': Select(attrs={'class': 'required selectpicker'}),
            'bill_print_type': Select(attrs={'class': 'required selectpicker'}),
            'gstin': TextInput(attrs={'class': 'form-control','placeholder' : 'GSTIN'}),
            'commission_per_packet': TextInput(attrs={'class': 'form-control required number','placeholder' : 'Commission Per Packet'}),
            'fssai_number': TextInput(attrs={'class': 'form-control','placeholder' : 'FSSAI Number'}),
        }
        error_messages = {
            'name' : {
                'required' : _("Name field is required."),
            },
            'email' : {
                'required' : _("Email field is required."),
            },
            'phone' : {
                'required' : _("Phone field is required."),
            },
            'address' : {
                'required' : _("Address field is required."),
            },
            'state' : {
                'required' : _("State field is required."),
            },
            'theme' : {
                'required' : _("Theme field is required."),
            },
            'commission_per_packet' : {
                'required' : _("Commission Per Packet field is required."),
            }
        }
