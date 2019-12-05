from django.conf.urls import url,include
import views

urlpatterns = [
    url(r'^$', views.customers, name='customers'),
    url(r'^view/(?P<pk>.*)/$', views.customer, name='customer'),

]
