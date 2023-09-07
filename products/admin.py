from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import Product


@admin.register(Product)
class ProductAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "price", "cost", "stock")
