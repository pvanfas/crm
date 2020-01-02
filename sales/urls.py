from django.conf.urls import url,include
from . import views

app_name = 'sales'

urlpatterns = [
    url(r'^create/$', views.create, name='create'),
    url(r'^edit/(?P<pk>.*)/$', views.edit, name='edit'),
    url(r'^$', views.sales, name='sales'),
    url(r'^view/(?P<pk>.*)/$', views.sale, name='sale'),
    url(r'^delete/(?P<pk>.*)/$', views.delete, name='delete'),

    url(r'^delete-selected-sale/$', views.delete_selected_sale, name='delete_selected_sale'),

]
