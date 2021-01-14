from django.urls import path, include
from django.contrib import admin
from main import views as general_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('',general_views.app,name='app'),
    path('app/',general_views.app,name='app'),
    path('app/dashboard/',general_views.dashboard,name='dashboard'),

    path('app/customers/', include('customers.urls',namespace='customers')),
    path('app/vendors/', include('vendors.urls',namespace='vendors')),
    path('app/products/', include('products.urls',namespace='products')),
    path('app/sales/', include('sales.urls',namespace='sales')),

    path('app/accounts/', include('registration.backends.default.urls')),
    path('app/users/', include('users.urls', namespace='users')),

    path('api/v1/customers/', include('api.v1.customers.urls',namespace='api_v1_customers')),
    path('api/v1/sales/', include('api.v1.sales.urls',namespace='api_v1_sales')),
    path('api/v1/auth/', include('api.v1.authentication.urls',namespace='api_v1_authentication')),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
