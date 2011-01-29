from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

FACEBOOK_PREPOPULATE_USER_DATA = getattr(settings, 'FACEBOOK_PREPOPULATE_USER_DATA', None)
FACEBOOK_EXTENDED_PERMISSIONS = getattr(settings, 'FACEBOOK_EXTENDED_PERMISSIONS', None)

class FacebookBackend(ModelBackend):
    """ Authenticate a facebook user. """
    def authenticate(self, fb_uid=None, fb_object=None):
        """ If we receive a facebook uid then the cookie has already been validated. """
        if fb_uid:
            user, created = User.objects.get_or_create(username=fb_uid)

            # Consider replacing this synchronous data request (out to Facebook
            # and back) with an asynchronous request, using Celery or similar tool
            if FACEBOOK_PREPOPULATE_USER_DATA and created and fb_object:
                fb_user = fb_object.graph.get_object(u'me')
                user.first_name = fb_user['first_name']
                user.last_name  = fb_user['last_name']

                if 'email' in FACEBOOK_EXTENDED_PERMISSIONS and 'email' in fb_user:
                    user.email = fb_user['email']
                    
                user.save()

            return user
        return None
