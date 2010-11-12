from django.conf import settings

class Facebook(object):
    def __init__(self, user=None):
        if user is None:
            self.uid = None
        else:
            self.uid = user['uid']
            self.user = user
            self.graph = facebook.GraphAPI(user['access_token'])



class FacebookDebugCookieMiddleware(object):
    """ Sets an imaginary cookie to make it easy to work from a development environment. """
    def process_request(self, request):
        cookie_name = "fbs_" + settings.FACEBOOK_APP_ID
        request.COOKIES[cookie_name] = settings.FACEBOOK_DEBUG_COOKIE
        return None


class FacebookDebugTokenMiddleware(object):
    """ Forces a specific access token to be used. """
    def process_request(self, request):
        fb_user = {
          'uid':u'212900950',
          'access_token':'2227470867|2.FkEuuS_4N9cqPqqjd_FaMg__.3600.1289257200-212900950|xK2pUhlDtAlO1jp_P4TCx8TeLog',
        }
        request.facebook = Facebook(fb_user)
        return None


class FacebookMiddleware(object):
    """ Transparently integrate Django accounts with Facebook. """


class TokenDebuggingMiddleware(object):
    def process_request(self, request):
