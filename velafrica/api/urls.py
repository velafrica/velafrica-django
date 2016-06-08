from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from velafrica.api import views


urlpatterns = patterns('',
    url(r'^$', views.api_root),
    url(r'^trackings/?$', views.TrackingList.as_view(), name="trackings"),
    url(r'^trackings/(?P<pk>[0-9]+)/?$', views.TrackingDetail.as_view(), name='trackings_detail'),

)

urlpatterns = format_suffix_patterns(urlpatterns)