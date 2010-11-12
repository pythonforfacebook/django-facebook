import facebook
from django.conf import settings

class DjangoFacebook(object):
    """ Simple accessor object for the Facebook user. """
    def __init__(self, user):
        if user is None:
            self.uid = None
        else:
            self.uid = user['uid']
            self.user = user
            self.graph = facebook.GraphAPI(user['access_token'])


class FacebookDebugCookieMiddleware(object):
    """ Sets an imaginary cookie to make it easy to work from a development environment. 
    
    This should be a raw string as is sent from a browser to the server, obtained by
    LiveHeaders, Firebug or similar. The middleware takes care of naming the cookie
    correctly. This should initialised before FacebookMiddleware.
    """
    def process_request(self, request):
        cookie_name = "fbs_" + settings.FACEBOOK_APP_ID
        request.COOKIES[cookie_name] = settings.FACEBOOK_DEBUG_COOKIE
        return None


class FacebookDebugTokenMiddleware(object):
    """ Forces a specific access token to be used.
    
    This should be used instead of FacebookMiddleware. Make sure you have
    FACEBOOK_DEBUG_UID and FACEBOOK_DEBUG_TOKEN set in your configuration.
    """
    def process_request(self, request):
        user = {
          'uid':settings.FACEBOOK_DEBUG_UID,
          'access_token':settings.FACEBOOK_DEBUG_TOKEN,
        }
        request.facebook = Facebook(user)
        return None


class FacebookMiddleware(object):
    """ Transparently integrate Django accounts with Facebook. """
    def process_request(self, request):
        user = facebook.get_user_from_cookie(request.COOKIES,
            settings.FACEBOOK_APP_ID, settings.FACEBOOK_SECRET_KEY)
        request.facebook = DjangoFacebook(user)
        return None

