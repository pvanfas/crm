from django.conf.urls import url,include
import views
from customers.views import CustomerAutocomplete

urlpatterns = [
    url(r'^create/$', views.create, name='create'),
    url(r'^edit/(?P<pk>.*)/$', views.edit, name='edit'),
    url(r'^$', views.customers, name='customers'),
    url(r'^view/(?P<pk>.*)/$', views.customer, name='customer'),
    url(r'^delete/(?P<pk>.*)/$', views.delete, name='delete'),
    url(r'^customer-autocomplete/$',CustomerAutocomplete.as_view(),name='customer_autocomplete',),
    url(r'^get-customer/$', views.get_customer, name='get_customer'),
]
