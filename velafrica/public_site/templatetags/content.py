from django import template
from velafrica.public_site.models import Content

register = template.Library()


@register.simple_tag
def get_content(key):
    if Content.objects.count() > 0:
        value = Content.objects.get(key=key)
        if value:
            return value.value
        else:
            return key
    else:
        return key
