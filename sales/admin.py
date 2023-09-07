from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import Sale


@admin.register(Sale)
class SaleAdmin(ImportExportActionModelAdmin):
    list_display = ("customer", "date", "total")
