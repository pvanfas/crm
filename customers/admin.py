from __future__ import unicode_literals
from .models import Customer
from import_export.admin import ImportExportActionModelAdmin
from django.contrib import admin


@admin.register(Customer)
class CustomerAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "phone", "email")
