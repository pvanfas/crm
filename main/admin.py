from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import Mode


@admin.register(Mode)
class ModeAdmin(ImportExportActionModelAdmin):
    list_display = ("readonly", "maintenance", "down")
