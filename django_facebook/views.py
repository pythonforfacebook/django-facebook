from django.http import HttpRequest
from django.views.generic.simple import direct_to_template

def debug(request):
  """ View to debug the current state of the users authentication. """
  return direct_to_template(request, 'debug.html', {
    'cookies':request.COOKIES,
    'user':request.user,
    'facebook':request.facebook,
    })
