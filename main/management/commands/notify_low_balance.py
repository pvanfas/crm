from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from main.functions import get_low_balance_limit, get_currency
from users.functions import send_email
from django.template.loader import render_to_string
from users.models import NotificationSubject, Notification


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        users = User.objects.filter(is_active=True,is_staff=False)
        
        low_balance_limit = get_low_balance_limit()
        for user in users:
            currency = get_currency(user)
            current_balance = user.accountbalance.balance
            
            if user.accountbalance.balance < low_balance_limit:
                email = user.email
                name = user.username
                template_name = 'email/email.html'
                subject = "Low Balance Alert | Arkboss"           
                content = "You have only %s %s in your Arkboss account. Please add some funds for uninterrupted service." %(currency,current_balance)
                context = {
                    'name' : name,
                    'subject' : subject,
                    'content' : content,
                    'email' : email
                }
                html_content = render_to_string(template_name,context) 
                send_email(email,subject,content,html_content) 
                
                #create low balance notification
                subject = NotificationSubject.objects.get(code="low_balance")
                create_notification(request,notification_type,instance=instance.product)
                
                