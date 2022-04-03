from __future__ import unicode_literals
from .models import Sale
from import_export.admin import ImportExportActionModelAdmin
from django.contrib import admin


@admin.register(Sale)
class SaleAdmin(ImportExportActionModelAdmin):
    list_display = ("customer", "date", "total")
