from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import Vendor


@admin.register(Vendor)
class VendorAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "phone", "email")
