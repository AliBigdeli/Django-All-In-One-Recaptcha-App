from django import template
from aio_recaptcha.app_settings import RECAPTCHAV3_SITE_KEY

register = template.Library()

@register.simple_tag(name='get_site_key')
def function():
    return RECAPTCHAV3_SITE_KEY
