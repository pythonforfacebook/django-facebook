from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import available_attrs
from django.utils.http import urlquote

def facebook_required(login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """ Check the user has a valid facebook connection. """
    if not login_url:
        from django.conf import settings
        login_url = settings.LOGIN_URL

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.facebook.uid:
                return view_func(request, *args, **kwargs)
            path = urlquote(request.get_full_path())
            tup = login_url, redirect_field_name, path
            #return HttpResponseRedirect('%s?%s=%s' % tup)
            return HttpResponse('You must be logged in with Facebook.')
        return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
