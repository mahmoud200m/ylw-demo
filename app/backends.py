from django.contrib.auth.models import check_password
from django.contrib.auth import get_user_model
import onetimepass as otp

"""
custom backend for the user authentication
"""
class SecureuthBackend(object):
    def authenticate(self, username=None, password=None,  secureKey=None):
        """ Authenticate a user based onu sername, password and secureKey. """
        try:
            User = get_user_model()
            user = User.objects.get(username=username)

            if user.check_password(password):
                my_secret = user.get_key()

                if( otp.valid_totp(token=secureKey, secret=my_secret) ):
                    return user
            return None 
        except User.DoesNotExist:
            return None 

        return None 

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            User = get_user_model()
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None