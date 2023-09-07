from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "phone", "email")
