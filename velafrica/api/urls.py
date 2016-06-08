# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from velafrica.api import views

tracking = patterns('',
    url(r'^trackings/?$', views.TrackingList.as_view(), name="trackings"),
    url(r'^trackings/(?P<pk>[0-9]+)/?$', views.TrackingDetail.as_view(), name='trackings_detail'),
    url(r'^trackingevents/?$', views.TrackingEventList.as_view(), name="trackingevents"),
    url(r'^trackingevents/(?P<pk>[0-9]+)/?$', views.TrackingEventDetail.as_view(), name='trackingevents'),
    url(r'^trackingeventtypes/?$', views.TrackingEventTypeList.as_view(), name="trackingeventtypes"),
    url(r'^trackingeventtypes/(?P<pk>[0-9]+)/?$', views.TrackingEventTypeDetail.as_view(), name='trackingeventtypes_detail'),
)

urlpatterns = patterns('',
    url(r'^$', views.api_root),
    url(r'^tracking/', include(tracking, namespace="tracking")),
)

urlpatterns = format_suffix_patterns(urlpatterns)