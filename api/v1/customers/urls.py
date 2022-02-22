from django.urls import path
from . import views

app_name = "customers"

urlpatterns = [
    path("", views.customers, name="customers"),
    path("view/<str:pk>/", views.customer, name="customer"),
    path("create/", views.create_customer, name="create_customer"),
    path("edit/<str:pk>/", views.edit_customer, name="edit_customer"),
]
