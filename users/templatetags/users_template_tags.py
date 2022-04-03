from django.contrib.auth.models import User
from django.template import Library

register = Library()


@register.filter
def get_user_name(username):
    name = "-"
    if User.objects.filter(username=username).exists():
        name = User.objects.get(username=username).username

    return name
