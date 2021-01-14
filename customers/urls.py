from django.urls import path,include
from . import views
from customers.views import CustomerAutocomplete

app_name = 'customers'

urlpatterns = [
    path('customer-autocomplete/',CustomerAutocomplete.as_view(),name='customer_autocomplete',),
    path('create/', views.create, name='create'),
    path('edit/<str:pk>/', views.edit, name='edit'),
    path('', views.customers, name='customers'),
    path('view/<str:pk>/', views.customer, name='customer'),
    path('delete/<str:pk>/', views.delete, name='delete'),

    path('get-customer/', views.get_customer, name='get_customer'),

    path('delete-selected-customer/', views.delete_selected_customer, name='delete_selected_customer'),

]
