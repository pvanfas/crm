from django.conf.urls import url,include
from . import views
from products.views import ProductAutocomplete

app_name = 'products'

urlpatterns = [
    url(r'^product-autocomplete/$',ProductAutocomplete.as_view(),name='product_autocomplete',),
    url(r'^create/$', views.create, name='create'),
    url(r'^edit/(?P<pk>.*)/$', views.edit, name='edit'),
    url(r'^$', views.products, name='products'),
    url(r'^view/(?P<pk>.*)/$', views.product, name='product'),
    url(r'^delete/(?P<pk>.*)/$', views.delete, name='delete'),

    url(r'^get-product/$', views.get_product, name='get_product'),
    url(r'^delete-selected-products/$', views.delete_selected_products, name='delete_selected_products'),


]
