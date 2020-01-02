# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2020-01-02 11:28
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('auto_id', models.PositiveIntegerField(db_index=True, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date', models.DateField()),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_sale_objects', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Customer')),
                ('updater', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='updator_sale_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date',),
                'db_table': 'sales_sale',
                'verbose_name': 'sale',
                'verbose_name_plural': 'sales',
            },
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Sale')),
            ],
            options={
                'ordering': ('sale',),
                'db_table': 'sales_sale item',
                'verbose_name': 'sale item',
                'verbose_name_plural': 'sale items',
            },
        ),
    ]
