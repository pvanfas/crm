from django.urls import path
from . import views
from vendors.views import VendorAutocomplete

app_name = 'vendors'

urlpatterns = [
    path('vendor-autocomplete/',VendorAutocomplete.as_view(),name='vendor_autocomplete',),
    path('create/', views.create, name='create'),
    path('edit/<str:pk>/', views.edit, name='edit'),
    path('', views.vendors, name='vendors'),
    path('view/<str:pk>/', views.vendor, name='vendor'),
    path('delete/<str:pk>/', views.delete, name='delete'),

    path('get-vendor/', views.get_vendor, name='get_vendor'),

    path('delete-selected-vendor/', views.delete_selected_vendor, name='delete_selected_vendor'),

]
