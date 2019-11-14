from __future__ import absolute_import
from celery import shared_task
from products.models import ProductExpiryDate
from users.models import NotificationSubject, Notification
import datetime
from django.contrib.auth.models import User
from staffs.models import Staff


@shared_task
def product_expiry_reminder_task(text):
    today = datetime.date.today()
    superusers = User.objects.filter(is_superuser=True, is_active=True)
    instances = ProductExpiryDate.objects.filter(is_deleted=False, expiry_date__gte=today)
    for instance in instances :
        if instance.product.product_expiry_before:
            to_date = today + datetime.timedelta(days=instance.product.product_expiry_before)
            if to_date <= instance.expiry_date :
                subject = NotificationSubject.objects.get(code="expiry_notification")
                for user in superusers:
                    Notification(user=user,subject=subject,product=instance.product,shop=instance.shop, is_active=True,expiry_date=instance).save() 
                staffs = Staff.objects.filter(is_deleted=False)
                for staff in staffs:
                    user = staff.user
                    if staff.permissionlist:
                        permlist = [str(x.code) for x in staff.permissions.all()]
                        if 'can_view_product' in permlist:
                            Notification(
                                user = staff.user,
                                subject = subject,
                                product = instance.product,
                                is_active = True,
                                shop = instance.shop,
                                expiry_date=instance
                            ).save()
    return "Completed"