from django import template
from django.conf import settings
register = template.Library()

@register.inclusion_tag('facebook_init.html')
def facebook_init():
  try:
    app_id = settings.FACEBOOK_APP_ID    
  except AttributeError:
    raise template.TemplateSyntaxError, "%r tag requires FACEBOOK_APP_ID to be configured." \
      % token.contents.split()[0]
 return {'app_id': app_id}