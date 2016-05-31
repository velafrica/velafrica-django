from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from velafrica.api import views


urlpatterns = patterns('',
    url(r'^$', views.api_root),

)

urlpatterns = format_suffix_patterns(urlpatterns)