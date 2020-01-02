from django.conf.urls import url,include
from . import views
from vendors.views import VendorAutocomplete

app_name = 'vendors'

urlpatterns = [
    url(r'^vendor-autocomplete/$',VendorAutocomplete.as_view(),name='vendor_autocomplete',),
    url(r'^create/$', views.create, name='create'),
    url(r'^edit/(?P<pk>.*)/$', views.edit, name='edit'),
    url(r'^$', views.vendors, name='vendors'),
    url(r'^view/(?P<pk>.*)/$', views.vendor, name='vendor'),
    url(r'^delete/(?P<pk>.*)/$', views.delete, name='delete'),

    url(r'^get-vendor/$', views.get_vendor, name='get_vendor'),

    url(r'^delete-selected-vendor/$', views.delete_selected_vendor, name='delete_selected_vendor'),

]
