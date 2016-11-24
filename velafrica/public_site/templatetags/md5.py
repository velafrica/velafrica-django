from django import template
from django.conf import settings
import hashlib

register = template.Library()


@register.filter(name='md5')
def md5_string(value):
    return hashlib.md5(value).hexdigest()
