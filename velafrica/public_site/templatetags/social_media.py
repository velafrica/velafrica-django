import urllib
from django import template
from django.conf import settings
from django.utils.functional import lazy
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def sharing_buttons(context, default_text=""):
    url = urllib.quote_plus(context.request.build_absolute_uri())
    onclick = "window.open(this.href,'targetWindow','toolbar=no,location=0,status=no,menubar=no,scrollbars=yes,resizable=yes,width=600,height=250'); return false"
    links = u'<a href="https://www.facebook.com/dialog/share?app_id={}&display=popup&href={}" target="_blank" onclick="{}">' \
            u'<img src="/static/img/facebook_orange.png" alt=""></a>' \
            u'<a href="https://twitter.com/intent/tweet?text={}&via=velafrica&url={}" target="_blank" onclick="{}">' \
            u'<img src="/static/img/twitter_orange.png" alt=""></a>'\
        .format(facebook_app_id(), url, onclick, urllib.quote_plus(default_text), url, onclick)
    return mark_safe(links)


@register.simple_tag()
def facebook_app_id():
    return getattr(settings, 'FACEBOOK_APP_ID', '')
