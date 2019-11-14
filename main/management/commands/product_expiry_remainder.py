from django.shortcuts import render, get_object_or_404
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from main.functions import get_low_balance_limit, get_currency
from users.functions import send_email
from django.template.loader import render_to_string
from users.models import NotificationSubject, Notification
from products.models import Product
import datetime
from main.tasks import product_expiry_reminder_task


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        product_expiry_reminder_task.delay('check expiry')
                    