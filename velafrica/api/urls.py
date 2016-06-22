# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from velafrica.api import utils
from velafrica.api import views

stock = [
    url(r'^warehouses/?$', views.WarehouseList.as_view(), name="warehouses"),
    url(r'^warehouses/(?P<pk>[0-9]+)/?$', views.WarehouseDetail.as_view(), name='warehouses_detail'),
]

organisation = [
    url(r'^organisations/?$', views.OrganisationList.as_view(), name="organisations"),
    url(r'^organisations/(?P<pk>[0-9]+)/?$', views.OrganisationDetail.as_view(), name='organisations_detail'),
]

tracking = [
    url(r'^trackings/?$', views.TrackingList.as_view(), name="trackings"),
    url(r'^trackings/(?P<pk>[0-9]+)/?$', views.TrackingDetail.as_view(), name='tracking'),
    url(r'^trackingevents/?$', views.TrackingEventList.as_view(), name="trackingevents"),
    url(r'^trackingevents/(?P<pk>[0-9]+)/?$', views.TrackingEventDetail.as_view(), name='trackingevent'),
    url(r'^trackingeventtypes/?$', views.TrackingEventTypeList.as_view(), name="trackingeventtypes"),
    url(r'^trackingeventtypes/(?P<pk>[0-9]+)/?$', views.TrackingEventTypeDetail.as_view(), name='trackingeventtype'),
    url(r'^velotypes/?$', views.VeloTypeList.as_view(), name="velotypes"),
    url(r'^velotypes/(?P<pk>[0-9]+)/?$', views.VeloTypeDetail.as_view(), name='velotype'),
]

# first attempt at generic views
velafrica_sud = [
    url(r'^container/?$', utils.get_listview('velafrica_sud', 'Container').as_view(), kwargs={'test':'test'}, name="containers"),
    url(r'^container/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('velafrica_sud', 'Container').as_view(), name='container'),
    url(r'^countries/?$', utils.get_listview('velafrica_sud', 'Country').as_view(), name='countries'),
    url(r'^countries/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('velafrica_sud', 'Country').as_view(), name='country'),
    url(r'^forwarders/?$', utils.get_listview('velafrica_sud', 'Forwarder').as_view(), name="forwarders"),
    url(r'^forwarders/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('velafrica_sud', 'Forwarder').as_view(), name='forwarder'),
    url(r'^partners/?$', utils.get_listview('velafrica_sud', 'PartnerSud').as_view(), name="partners"),
    url(r'^partners/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('velafrica_sud', 'PartnerSud').as_view(), name='partner'),
]

# where it all comes together
urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^organisation/', include(organisation, namespace="organisation")),
    url(r'^stock/', include(stock, namespace="stock")),
    url(r'^tracking/', include(tracking, namespace="tracking")),
    url(r'^velafrica_sud/', include(velafrica_sud, namespace="velafrica_sud")),
]

urlpatterns = format_suffix_patterns(urlpatterns)