from django.db import models
from main.models import BaseModel
from versatileimagefield.fields import VersatileImageField


class Customer(BaseModel):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    email = models.EmailField()
    address = models.TextField()
    photo = VersatileImageField("Photo", blank=True, null=True, upload_to="customers/")

    class Meta:
        ordering = ("-date_added", "name")

    def __str__(self):
        return str(self.name)
