from django import template
from django.db.models import Q
from velafrica.public_site.models import TeamMember
register = template.Library()


@register.simple_tag()
def get_teammember(value):
    if TeamMember.objects.count() > 0:
        member = TeamMember.objects.filter(name=value)
        if member.count() >= 1:
            return member.first()
        else:
            return ''
    else:
        return ''
