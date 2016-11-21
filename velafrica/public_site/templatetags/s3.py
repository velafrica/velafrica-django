from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag()
def s3(path):
    return u"{}/{}".format(settings.AWS_S3_CUSTOM_DOMAIN, path)
