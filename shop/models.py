from django.db import models
from versatileimagefield.fields import VersatileImageField


class Shop(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    gstin = models.CharField(max_length=128)
    email = models.EmailField()
    address = models.TextField()
    account_name = models.CharField(max_length=128)
    account_number = models.CharField(max_length=128)
    ifsc = models.CharField(max_length=128)
    sales_person = models.CharField(max_length=128)
    job = models.CharField(max_length=128)
    shipping_method = models.CharField(max_length=128, default="")
    shipping_terms = models.CharField(max_length=128, default="")
    payment_terms = models.CharField(max_length=128, default="")
    logo = VersatileImageField("Logo", blank=True, null=True, upload_to="shop/")

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return str(self.name)
