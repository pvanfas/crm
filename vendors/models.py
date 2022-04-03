# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField

from main.models import BaseModel


class Vendor(BaseModel):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    email = models.EmailField()
    address = models.TextField()
    photo = VersatileImageField("Photo", blank=True, null=True, upload_to="vendors/")

    class Meta:
        ordering = ("-date_added", "name")

    def __str__(self):
        return str(self.name)
