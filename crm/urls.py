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
    
    url(r'^manifest\.json$',TemplateView.as_view(template_name="manifest.json",content_type="text/javascript"),name='manifest'),
    url(r'^sw\.js$',TemplateView.as_view(template_name="sw.js",content_type="text/javascript"),name='sw'),

    url(r'^$',general_views.app,name='app'),
    url(r'^app/$',general_views.app,name='app'),
    url(r'^app/dashboard/$',general_views.dashboard,name='dashboard'),

    url(r'^app/accounts/', include('registration.backends.default.urls')),
    url(r'^app/users/', include('users.urls', namespace="users")),
    url(r'^app/customers/', include('customers.urls', namespace="customers")),
    url(r'^app/products/', include('products.urls', namespace="products")),
    url(r'^app/sales/', include('sales.urls', namespace="sales")),

    url(r'^media/(?P<path>.*)$', serve, { 'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, { 'document_root': settings.STATIC_FILE_ROOT}),
]
