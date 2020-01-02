from django.conf.urls import url
from . import views

app_name = 'sales'

urlpatterns = [

    url(r'^$', views.sales, name='sales'),
    url(r'^view/(?P<pk>.*)/$', views.sale, name='sale'),
]
