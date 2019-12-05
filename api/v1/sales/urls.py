from django.conf.urls import url,include
import views

urlpatterns = [
    url(r'^$', views.sales, name='sales'),
    url(r'^view/(?P<pk>.*)/$', views.sale, name='sale'),

]
