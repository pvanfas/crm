from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    path("create/", views.create, name="create"),
    path("edit/<str:pk>/", views.edit, name="edit"),
    path("", views.sales, name="sales"),
    path("view/<str:pk>/", views.sale, name="sale"),
    path("delete/<str:pk>/", views.delete, name="delete"),
    path(
        "delete-selected-sale/", views.delete_selected_sale, name="delete_selected_sale"
    ),
]
