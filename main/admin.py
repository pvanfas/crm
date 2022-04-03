from __future__ import unicode_literals
from .models import Mode
from import_export.admin import ImportExportActionModelAdmin
from django.contrib import admin


@admin.register(Mode)
class ModeAdmin(ImportExportActionModelAdmin):
    list_display = ("readonly", "maintenance", "down")
