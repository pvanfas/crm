from __future__ import unicode_literals

from django.contrib import admin

from shop.models import Shop


class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "gstin", "email", "address")


admin.site.register(Shop, ShopAdmin)
