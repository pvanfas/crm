# INITIAL SETUP -------------------------------------------------------------------

# initialize project
cd dev/django/crm
virtualenv venv
source venv/bin/activate
cd src/crm
pip install -r r.txt

# Create database
sudo su postgres
createdb crm
createuser anfas -P
psql
grant all privileges on database crm to anfas;
\q
exit

# Migrate changes
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata initial_data user_groups permissions notification
python manage.py createsuperuser
python manage.py runserver
python manage.py dumpdata > database.json


# CUSTOMER MODEL -------------------------------------------------------------------

python manage.py startapp customers

# Define customer view
class Customer(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    email = models.EmailField()
    adress = models.TextField()

    class Meta:
        db_table = 'customers_customer'
        verbose_name = _('customer')
        verbose_name_plural = _('customers')
        ordering = ('-date_added','name')

    def __unicode__(self):
        return str(self.name)

# Add to main/BaseModel
is_deleted = models.BooleanField(default=False)

# Create customers/forms.py
from django import forms
from django.forms.widgets import TextInput, Textarea, Select
from django.utils.translation import ugettext_lazy as _
from customers.models import Customer


class CustomerForm(BaseModel):
    class Meta:
        model = Customer
        exclude = ['auto_id','creator','updater','is_deleted']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Name'}),
            'email': TextInput(attrs={'class': 'required email form-control','placeholder' : 'Email'}),
            'phone': TextInput(attrs={'class': 'required form-control','placeholder' : 'Phone'}),
            'address': Textarea(attrs={'class': 'required form-control','placeholder' : 'Address'}),
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
                'required' : _("Addess field is required."),
            },
        }
# add to crm/urls.py
    url(r'^app/customers/', include('customers.urls', namespace="customers")),

# Create customers/urls.py
from django.conf.urls import url,include
import views

urlpatterns = [
    url(r'^create/$', views.create, name='create'),
]

# Define customers/views.py
from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from main.decorators import check_mode, ajax_required
from main.functions import get_auto_id, generate_form_errors, get_a_id
import json
from django.views.decorators.http import require_GET
from users.models import NotificationSubject, Notification
from django.db.models import Sum
from django.contrib.auth.models import Group
import datetime
from calendar import monthrange
from django.utils import timezone
from decimal import Decimal


def create(request):
	return HttpResponse("hello")

# CREATE CUSTOMER FORM
from customers.models import Customer
from customers.forms import CustomerForm


def create(request):
    form = CustomerForm()
    context = {
        "form" : form,
        "title" : "Create Customer",

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

    return render(request,"customers/entry.html", context)

# customers.models
from django.utils.translation import ugettext_lazy as _
# Installed apps
'customers'
# Define associated urls
urlpatterns = [
    url(r'^create/$', views.create, name='create'),
    url(r'^edit/(?P<pk>.*)/$', views.edit, name='edit'),
    url(r'^$', views.customers, name='customers'),
    url(r'^view/(?P<pk>.*)/$', views.customer, name='customer'),
    url(r'^delete/(?P<pk>.*)/$', views.delete, name='delete'),
]
# Define view for each
def edit(request,pk):
    pass


def customers(request):
    pass


def customer(request,pk):
    pass


def delete(request,pk):
    pass

# Edit template and add more fields

# Adding GET & POST actions, Define value for data.creator,updator
def create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = get_auto_id(Customer)
            form.save()
             
            response_data = {
                 "status" : "true",
                 "title" : "Successfully Created",
                 "message" : "Customer successfully created",
                 # "redirect" : 'true',
                 # "redirect_url" : reverse('customers:customer',kwargs={"pk":data.pk})
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

        form = CustomerForm()
        context = {
            "form" : form,
            "title" : "Create Customer",
            # "redirect" : True,

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

        return render(request,"customers/entry.html", context)

# Define reddirect scheme, Define Customer list, 404
def customer(request,pk):
    instance = get_object_or_404(Customer.objects.filter(pk=pk))
    context = {
        "title" : "Customer : " + instance.name,
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

    return render(request, 'customers/customer.html', context)

# Adding additional fields in templates
# Add links to menu

# Edit view
# instance=instance gives edit functionality
def edit(request,pk):
    if request.method == "POST":
        form = CustomerForm(request.POST,instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.updater = request.user
            date_updated = datetime.datetime.now()
            form.save()
             
            response_data = {
                 "status" : "true",
                 "title" : "Successfully Updated",
                 "message" : "Customer successfully Updated",
                 "redirect" : 'true',
                 "redirect_url" : reverse('customers:customers',kwargs={"pk":data.pk})
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
        instance = get_object_or_404(Customer.objects.filter(pk=pk))
        form = CustomerForm(instance=instance)
        context = {
            "form" : form,
            "title" : "Create Customer",
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

        return render(request,"customers/entry.html", context)