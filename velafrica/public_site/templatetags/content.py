from django import template
from django.conf import settings
from django.db.models import Q
from velafrica.public_site.models import Content

register = template.Library()

@register.simple_tag(takes_context=True)
def get_content(context, key, description=''):
    # return context.request.LANGUAGE_CODE
    path = 'index'
    if context.request.path != '/':
        path = context.request.path.replace('/', '_')

    language = context.request.LANGUAGE_CODE


    full_key = u"{}_{}_{}".format(
        language,
        path,
        key
    )
    value = None
    value_set = False
    if not Content.objects.filter(Q(language=language) & Q(path=path) & Q(key=key)).count() > 0:
        for lang_code, lang in settings.LANGUAGES:
            key_value = Content(
                language=lang_code,
                path=path,
                key=key,
                description=description
            )
            key_value.save()
            if lang == language:
                value = key_value
                value_set = True

    if not value_set:
        value = Content.objects.get(
            language=language,
            path=path,
            key=key
        )

    if value.value:
        return value.value
    else:
        return full_key
