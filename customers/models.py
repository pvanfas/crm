# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from main.models import BaseModel
from versatileimagefield.fields import VersatileImageField

class Customer(BaseModel):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    email = models.EmailField()
    address = models.TextField()
    photo = VersatileImageField('Photo',blank=True,null=True,upload_to="customers/")

    class Meta:
        db_table = 'customers_customer'
        verbose_name = _('customer')
        verbose_name_plural = _('customers ')
        ordering = ('-date_added','name',)

    def __str__(self):
        return str(self.name)
