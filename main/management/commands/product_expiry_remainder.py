from django.core.management.base import BaseCommand
from main.tasks import product_expiry_reminder_task


class Command(BaseCommand):
    def handle(self, *args, **options):

        product_expiry_reminder_task.delay("check expiry")
