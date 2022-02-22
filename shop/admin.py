from __future__ import unicode_literals
from django.contrib import admin
from shop.models import Shop


class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "gstin", "email", "address")


admin.site.register(Shop, ShopAdmin)

# to change admin header
admin.site.site_header = "Fresh 8 Admininistration"
admin.site.site_title = "Fresh 8 Admin Portal"
admin.site.index_title = "Welcome to Fresh 8 Researcher Portal"
