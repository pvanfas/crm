from django.conf.urls import url,include
import views
from customers.views import CustomerAutocomplete


urlpatterns = [
    url(r'^customer-autocomplete/$',CustomerAutocomplete.as_view(),name='customer_autocomplete',),
    url(r'^create/$', views.create, name='create'),
    url(r'^edit/(?P<pk>.*)/$', views.edit, name='edit'),
    url(r'^$', views.sales, name='sales'),
    url(r'^view/(?P<pk>.*)/$', views.sale, name='sale'),
    url(r'^delete/(?P<pk>.*)/$', views.delete, name='delete'),
]
