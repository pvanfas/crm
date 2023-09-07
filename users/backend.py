import re

from django.contrib.auth import get_user_model
from django.dispatch import receiver
from registration.signals import user_registered


User = get_user_model()


class EmailOrUsernameModelBackend(object):
    def authenticate(self, request, username=None, password=None):
        # Check if the username is an email address
        if re.match(r"[^@]+@[^@]+\.[^@]+", username):
            kwargs = {"email": username}
        else:
            kwargs = {"username": username}

        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


@receiver(user_registered)
def user_created(sender, user, request, **kwargs):
    # Generate a unique identifier for the user (e.g., 'f3_user_idab')
    f3 = user.username[:3]
    user_id = str(user.id)
    unique_identifier = f3 + user_id + "ab"
    user.profile.unique_identifier = unique_identifier
    user.profile.save()
