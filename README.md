Facebook integration for your Django website
=============================================

Installation:
------------
Simply add ``django_facebook`` to your INSTALLED_APPS and configure
the following settings:

    FACEBOOK_APP_ID = ''
    FACEBOOK_API_KEY = ''
    FACEBOOK_SECRET_KEY = ''

    # Optionally set default permissions to request, e.g: ['email', 'user_about_me']
    FACEBOOK_PERMS = []
    
    # And for local debugging, use one of the debug middlewares and set:
    FACEBOOK_DEBUG_TOKEN = ''
    FACEBOOK_DEBUG_UID = ''
    FACEBOOK_DEBUG_COOKIE = ''
    FACEBOOK_DEBUG_SIGNEDREQ = ''


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

You may find the ``facebook_perms`` tag useful, which takes the setting
in FACEBOOK_PERMISSIONS and prints the extended permissions out
in a comma-separated list.

    <fb:login-button show-faces="false" width="200" max-rows="1"
      perms="{% facebook_perms %}"></fb:login-button>


A helpful debugging page to view the status of your facebook login can
be enabled by adding this to your url configuration:

    (r'^facebook_debug/', direct_to_template, {'template':'facebook_debug.html'}),  


Once this is in place you are ready to start with the facebook javascript SDK!

This module also provides all of the tools necessary for working with facebook
on the backend:


Middleware:
----------
This provides seamless access to the Facebook Graph via request object.

If a user accesses your site with:
- a valid cookie (Javascript SDK), or
- a valid ``signed_request`` parameter (Facebook Canvas App),
then your views will have access to request.facebook.graph and you can
begin querying the graph immediately. For example, to get the users friends:

    def friends(request):
      if request.facebook:
        friends = request.facebook.graph.get_connections('me', 'friends')
        
To use the middleware, simply add this to your MIDDLEWARE_CLASSES:
    'django_facebook.middleware.FacebookMiddleware'


``FacebookDebugCookieMiddleware`` allows you to set a cookie in your settings
file and use this to simulate facebook logins offline.

``FacebookDebugTokenMiddleware`` allows you to set a uid and access_token to
force facebook graph availability.

``FacebookDebugCanvasMiddleware`` allows you to set a signed_request to mimic
a page being loaded as a canvas inside Facebook.


Authentication:
--------------
This provides seamless integration with the Django user system.

If a user accesses your site with a valid facebook cookie, a user
account is automatically created or retrieved based on the facebook UID.

To use the backend, add this to your AUTHENTICATION_BACKENDS:
    'django_facebook.auth.FacebookBackend'

To automatically populate your User and Profile models with facebook data, use:
    'django_facebook.auth.FacebookProfileBackend'
  
Don't forget to include the default backend if you want to use standard
logins for users as well:
    'django.contrib.auth.backends.ModelBackend'


Decorators:
----------
``@facebook_required`` is a decorator which ensures the user is currently
logged in with facebook and has access to the facebook graph. It is a replacement
for ``@login_required`` if you are not using the facebook authentication backend.

``@canvas_required`` is a decorater to ensure the view is being loaded with
a valid ``signed_request`` via Facebook Canvas. If signed_request is not found, the
decorator will return a HTTP 400. If signed_request is found but the user has not
authorised, the decorator will redirect the user to authorise.
