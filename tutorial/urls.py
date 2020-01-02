from django.conf.urls import url, include
from django.contrib import admin
from main import views as general_views
from django.conf import settings
from registration.backends.default.views import RegistrationView
from users.forms import RegForm
from users.backend import user_created
from django.views.static import serve
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),

    url(r'^api/v1/customers/', include('api.v1.customers.urls',namespace="api_v1_customers")),
    url(r'^api/v1/sales/', include('api.v1.sales.urls',namespace="api_v1_sales")),
    url(r'^api/v1/auth/', include('api.v1.authentication.urls',namespace="api_v1_authentication")),

    url(r'^$',general_views.app,name='app'),
    url(r'^app/$',general_views.app,name='app'),
    url(r'^app/dashboard/$',general_views.dashboard,name='dashboard'),

    url(r'^app/customers/', include('customers.urls',namespace="customers")),
    url(r'^app/vendors/', include('vendors.urls',namespace="vendors")),
    url(r'^app/products/', include('products.urls',namespace="products")),
    url(r'^app/sales/', include('sales.urls',namespace="sales")),

    url(r'^app/accounts/', include('registration.backends.default.urls')),
    url(r'^app/users/', include('users.urls', namespace="users")),

    url(r'^media/(?P<path>.*)$', serve, { 'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, { 'document_root': settings.STATIC_FILE_ROOT}),


]
