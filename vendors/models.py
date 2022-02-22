# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import gettext_lazy as _
from main.models import BaseModel
from versatileimagefield.fields import VersatileImageField


class Vendor(BaseModel):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    email = models.EmailField()
    address = models.TextField()
    photo = VersatileImageField("Photo", blank=True, null=True, upload_to="vendors/")

    class Meta:
        db_table = "vendors_vendor"
        verbose_name = _("vendor")
        verbose_name_plural = _("vendors ")
        ordering = ("-date_added", "name")

    def __str__(self):
        return str(self.name)
