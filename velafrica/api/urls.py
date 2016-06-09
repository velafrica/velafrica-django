# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from velafrica.api import views



stock = patterns('',
    url(r'^warehouses/?$', views.WarehouseList.as_view(), name="warehouses"),
    url(r'^warehouses/(?P<pk>[0-9]+)/?$', views.WarehouseDetail.as_view(), name='warehouses_detail'),
)

organisation = patterns('',
    url(r'^organisations/?$', views.OrganisationList.as_view(), name="organisations"),
    url(r'^organisations/(?P<pk>[0-9]+)/?$', views.OrganisationDetail.as_view(), name='organisations_detail'),
)

tracking = patterns('',
    url(r'^trackings/?$', views.TrackingList.as_view(), name="trackings"),
    url(r'^trackings/(?P<pk>[0-9]+)/?$', views.TrackingDetail.as_view(), name='trackings_detail'),
    url(r'^trackingevents/?$', views.TrackingEventList.as_view(), name="trackingevents"),
    url(r'^trackingevents/(?P<pk>[0-9]+)/?$', views.TrackingEventDetail.as_view(), name='trackingevents'),
    url(r'^trackingeventtypes/?$', views.TrackingEventTypeList.as_view(), name="trackingeventtypes"),
    url(r'^trackingeventtypes/(?P<pk>[0-9]+)/?$', views.TrackingEventTypeDetail.as_view(), name='trackingeventtypes_detail'),
    url(r'^velotypes/?$', views.VeloTypeList.as_view(), name="velotypes"),
    url(r'^velotypes/(?P<pk>[0-9]+)/?$', views.VeloTypeDetail.as_view(), name='velotypes_detail'),
)

# where it all comes together
urlpatterns = patterns('',
    url(r'^$', views.api_root),
    url(r'^organisation/', include(organisation, namespace="organisation")),
    url(r'^stock/', include(stock, namespace="stock")),
    url(r'^tracking/', include(tracking, namespace="tracking")),
)

urlpatterns = format_suffix_patterns(urlpatterns)