from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class FacebookBackend(ModelBackend):
    """ Authenticate a facebook user. """
    def authenticate(self, fb_uid=None):
        """ If we receive a facebook uid then the cookie has already been validated. """
        if fb_uid:
          user, created = User.objects.get_or_create(username=fb_uid)
          return user
        return None