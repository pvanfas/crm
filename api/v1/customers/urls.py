from django.conf.urls import url
from . import views

app_name = 'customers'

urlpatterns = [

    url(r'^$', views.customers, name='customers'),
    url(r'^view/(?P<pk>.*)/$', views.customer, name='customer'),
    url(r'^create/$', views.create_customer, name='create_customer'),
    url(r'^edit/(?P<pk>.*)/$', views.edit_customer, name='edit_customer'),

]
