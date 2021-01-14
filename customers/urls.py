from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.customers, name='customers'),
    path('create/', views.create, name='create'),
    path('edit/<str:pk>/', views.edit, name='edit'),
    path('view/<str:pk>/', views.customer, name='customer'),
    path('delete/<str:pk>/', views.delete, name='delete'),
    path('get-customer/', views.get_customer, name='get_customer'),
    path('delete-selected-customer/', views.delete_selected_customer, name='delete_selected_customer'),
]
