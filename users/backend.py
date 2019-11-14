from django.contrib.auth.models import User
from users.forms import RegistrationForm
from registration.signals import user_registered


class EmailOrUsernameModelBackend(object):
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
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
             
        
class AttemptCount(object):
    pass


def user_created(sender, user, request, **kwargs):
    
    f3 = user.username[:3]
    user_id = str(user.id)
    invite_code = f3 + user_id + 'ab'

user_registered.connect(user_created)


