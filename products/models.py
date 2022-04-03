# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=128)
    price = models.DecimalField(
        default=0.0,
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    cost = models.DecimalField(
        default=0.0,
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    stock = models.DecimalField(
        default=0.0,
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    class Meta:
        ordering = ("-date_added", "name")

    def __str__(self):
        return str(self.name)
