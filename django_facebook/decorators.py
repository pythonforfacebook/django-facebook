from functools import update_wrapper, wraps
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import available_attrs
from django.utils.http import urlquote
        
def facebook_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    def _passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
        if not login_url:
            from django.conf import settings
            login_url = settings.LOGIN_URL
    
        def decorator(view_func):
            def _wrapped_view(request, *args, **kwargs):
                if test_func(request):
                    return view_func(request, *args, **kwargs)
                path = urlquote(request.get_full_path())
                tup = login_url, redirect_field_name, path
                return HttpResponse('You must have a current Facebook session to access this page.')
                # return HttpResponseRedirect('%s?%s=%s' % tup)
            return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
        return decorator

    actual_decorator = _passes_test(
        lambda r: r.facebook.uid,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator
