from __future__ import unicode_literals
from django.db import models
from main.models import BaseModel
from django.core.validators import MinValueValidator
from decimal import Decimal


class Sale(BaseModel):
    customer = models.ForeignKey(
        "customers.Customer",
        limit_choices_to={"is_deleted": False},
        on_delete=models.CASCADE,
    )
    date = models.DateField()
    sub_total = models.DecimalField(
        default=0.0,
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    discount = models.DecimalField(
        default=0.0,
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    total = models.DecimalField(
        default=0.0,
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    class Meta:
        db_table = "sales_sale"
        verbose_name = "sale"
        verbose_name_plural = "sales"
        ordering = ("-date",)

    def __str__(self):
        return str(self.auto_id)


class SaleItem(models.Model):
    sale = models.ForeignKey("sales.Sale", on_delete=models.CASCADE)
    product = models.ForeignKey(
        "products.Product",
        limit_choices_to={"is_deleted": False},
        on_delete=models.CASCADE,
    )
    qty = models.DecimalField(
        default=0.0,
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    class Meta:
        db_table = "sales_sale item"
        verbose_name = "sale item"
        verbose_name_plural = "sale items"
        ordering = ("sale",)

    def sub_total(self):
        return self.qty * self.product.price

    def __str__(self):
        return str(self.sale.auto_id)
