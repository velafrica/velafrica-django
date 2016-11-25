from django import template
import locale
register = template.Library()


@register.filter(name='swissint')
def swissint(value):
    if not value:
        return '0'
    return value.replace('.', "&#8217;")

