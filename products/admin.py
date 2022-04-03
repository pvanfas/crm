from __future__ import unicode_literals
from .models import Product
from import_export.admin import ImportExportActionModelAdmin
from django.contrib import admin


@admin.register(Product)
class ProductAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "price", "cost", "stock")
