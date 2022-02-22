from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("create/", views.create, name="create"),
    path("edit/<str:pk>/", views.edit, name="edit"),
    path("", views.products, name="products"),
    path("view/<str:pk>/", views.product, name="product"),
    path("delete/<str:pk>/", views.delete, name="delete"),
    path("get-product/", views.get_product, name="get_product"),
    path(
        "delete-selected-products/",
        views.delete_selected_products,
        name="delete_selected_products",
    ),
]
