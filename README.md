Facebook integration with your Django website
=============================================

Installation:
------------
Simply add ``django_facebook`` to your INSTALLED_APPS and configure
the following settings:

    FACEBOOK_APP_ID = ''
    FACEBOOK_API_KEY = ''
    FACEBOOK_SECRET_KEY = ''
    
    # Optionally for debugging
    FACEBOOK_DEBUG_COOKIE = ''
    FACEBOOK_DEBUG_TOKEN = ''


Templates:
---------
A few helpers for using the Javascript SDK can be enabled by adding
this to your base template in the ``<head>`` section:

    {% load facebook %}
    {% facebook_init %}
      {% block facebook_code %}{% endblock %}
    {% endfacebook %}

And this should be added just before your ``</html>`` tag:

    {% facebook_load %}
    
The ``facebook_load`` template tag inserts the code required to
asynchronously load the facebook javascript SDK. The ``facebook_init``
tag calls ``FB.init`` with your configured application settings. It is
best to put your facebook related javascript into the ``facebook_code``
region so that it can be called by the asynchronous handler.


A helpful debugging page to view the status of your facebook login can
be enabled by adding this to your url configuration:

    (r'^facebook_debug/', direct_to_template, {'template':'facebook_debug.html'}),  


Once this is in place you are ready to start with the facebook javascript SDK!

This module also provides all of the tools necessary for working with facebook
on the backend:


Middleware:
----------
This provides seamless access to the Facebook Graph via request object.

If a user accesses your site with a valid facebook cookie, your views
will have access to request.facebook.graph and you can begin querying
the graph immediately. For example, to get the users friends:

    def friends(request):
      if request.facebook:
        friends = request.facebook.graph.get_connections('me', 'friends')
        
To use the middleware, simply add this to your MIDDLEWARE_CLASSES:
    'django_facebook.middleware.FacebookMiddleware'


``FacebookDebugCookieMiddleware`` allows you to set a cookie in your settings
file and use this to simulate facebook logins offline.

``FacebookDebugTokenMiddleware`` allows you to set a uid and access_token to
force facebook graph availability.


Authentication:
--------------
This provides seamless integration with the Django user system.

If a user accesses your site with a valid facebook cookie, a user
account is automatically created or retrieved based on the facebook UID.

To use the backend, add this to your AUTHENTICATION_BACKENDS:
    'django_facebook.auth.FacebookBackend'
  
Don't forget to include the default backend if you want to use standard
logins for users as well:
    'django.contrib.auth.backends.ModelBackend'


Decorators:
----------
``@facebook_required`` is a decorator which ensures the user is currently
logged in with facebook and has access to the facebook graph. It is a replacement
for ``@login_required`` if you are not using the facebook authentication backend.
