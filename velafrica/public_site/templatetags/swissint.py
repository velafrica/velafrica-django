from django import template
import locale
register = template.Library()


@register.filter(name='swissint')
def swissint(value):
    return value.replace('.', "&#8217;")

