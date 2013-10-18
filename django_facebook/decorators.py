from functools import wraps

import facebook
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import (HttpResponse,
                         HttpResponseRedirect,
                         HttpResponseBadRequest)
from django.utils.decorators import available_attrs
from django.utils.http import urlquote
from django.conf import settings
from exceptions import (MissingSignedRequestException,
                        InvalidSignedRequestException)


def canvas_only(function=None):
    """
    Decorator ensures that a page is only accessed from within a facebook
    application.

    """

    def _dec(view_func):
        def _view(request, *args, **kwargs):
            # Make sure we're receiving a signed_request from facebook
            if not request.POST.get('signed_request'):
                if hasattr(settings, 'FACEBOOK_RAISE_SR_EXCEPTIONS') \
                   and settings.FACEBOOK_RAISE_SR_EXCEPTIONS:
                    raise MissingSignedRequestException(
                        'Signed request token missing'
                    )
                else:
                    return HttpResponseBadRequest(
                        '<h1>400 Bad Request</h1>'
                        '<p>Missing <em>signed_request</em>.</p>'
                    )

            # Parse the request and ensure it's valid
            signed_request = request.POST["signed_request"]
            data = facebook.parse_signed_request(signed_request,
                                                 settings.FACEBOOK_SECRET_KEY)
            if data is False:
                if hasattr(settings, 'FACEBOOK_RAISE_SR_EXCEPTIONS') \
                   and settings.FACEBOOK_RAISE_SR_EXCEPTIONS:
                    raise InvalidSignedRequestException(
                        'Signed request token does not parse'
                    )
                else:
                    return HttpResponseBadRequest(
                        '<h1>400 Bad Request</h1>'
                        '<p>Malformed <em>signed_request</em>.</p>'
                    )

            # If the user has not authorised redirect them
            if not data.get('user_id'):
                scope = getattr(settings, 'FACEBOOK_SCOPE', None)
                auth_url = facebook.auth_url(settings.FACEBOOK_APP_ID,
                                             settings.FACEBOOK_CANVAS_PAGE,
                                             scope)
                markup = ('<script type="text/javascript">'
                          'top.location.href="%s"</script>' % auth_url)
                return HttpResponse(markup)

            # Success so return the view
            return view_func(request, *args, **kwargs)

        return _view

    return _dec(function)


def facebook_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.

    """

    def _passes_test(test_func, login_url=None,
                     redirect_field_name=REDIRECT_FIELD_NAME):
        if not login_url:
            login_url = settings.LOGIN_URL

        def decorator(view_func):
            def _wrapped_view(request, *args, **kwargs):
                if test_func(request):
                    return view_func(request, *args, **kwargs)
                path = urlquote(request.get_full_path())
                tup = login_url, redirect_field_name, path
                return HttpResponseRedirect('%s?%s=%s' % tup)

            return wraps(view_func, assigned=available_attrs(view_func))(
                _wrapped_view)

        return decorator

    actual_decorator = _passes_test(
        lambda r: r.facebook,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator
