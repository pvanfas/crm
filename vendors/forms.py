from django import forms
from django.forms.widgets import Textarea, TextInput
from django.utils.translation import gettext_lazy as _

from vendors.models import Vendor


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        exclude = ["creator", "updater", "auto_id", "is_deleted"]
        widgets = {
            "name": TextInput(
                attrs={"class": "required form-control", "placeholder": "Name"}
            ),
            "email": TextInput(
                attrs={"class": "required form-control email", "placeholder": "Email"}
            ),
            "phone": TextInput(
                attrs={"class": "required form-control", "placeholder": "Phone"}
            ),
            "address": Textarea(
                attrs={"class": "required form-control", "placeholder": "Address"}
            ),
        }
        error_messages = {
            "name": {"required": _("Name field is required.")},
            "email": {"required": _("Email field is required.")},
            "phone": {"required": _("Phone field is required.")},
            "address": {"required": _("Address field is required.")},
        }
