# -*- coding: utf-8 -*-
from django.conf.urls import include, patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from velafrica.api import utils
from velafrica.api import views


collection = [
    url(r'^eventcategories/?$', utils.get_listview('collection', 'EventCategory').as_view(), name="eventcategories"),
    url(r'^eventcategories/(?P<pk>[0-9]+)/?$', utils.get_listview('collection', 'EventCategory').as_view(), name='eventcategory'),
    url(r'^events/?$', utils.get_listview('collection', 'Event').as_view(), name="events"),
    url(r'^events/(?P<pk>[0-9]+)/?$', utils.get_listview('collection', 'Event').as_view(), name='event'),
    url(r'^tasks/?$', utils.get_listview('collection', 'Task').as_view(), name="tasks"),
    url(r'^tasks/(?P<pk>[0-9]+)/?$', utils.get_listview('collection', 'Task').as_view(), name='tasks'),
    url(r'^taskprogresses/?$', utils.get_listview('collection', 'TaskProgress').as_view(), name="tasksprogresses"),
    url(r'^taskprogresses/(?P<pk>[0-9]+)/?$', utils.get_listview('collection', 'TaskProgress').as_view(), name='taskprogress'),
    url(r'^collectionevents/?$', utils.get_listview('collection', 'CollectionEvent').as_view(), name="collectionevents"),
    url(r'^collectionevents/(?P<pk>[0-9]+)/?$', utils.get_listview('collection', 'CollectionEvent').as_view(), name='collectionevent'),
]

counter = [
    url(r'^entries/?$', utils.get_listview('counter', 'Entry').as_view(), name="entries"),
    url(r'^entries/(?P<pk>[0-9]+)/?$', utils.get_listview('counter', 'entry').as_view(), name='entry'),
]

stock = [
    url(r'^warehouses/?$', views.WarehouseList.as_view(), name="warehouses"),
    url(r'^warehouses/(?P<pk>[0-9]+)/?$', views.WarehouseDetail.as_view(), name='warehouses_detail'),

    url(r'^products/?$', utils.get_listview('stock', 'Product').as_view(), name="products"),
    url(r'^products/(?P<pk>[0-9]+)/?$', utils.get_listview('stock', 'Product').as_view(), name='product'),
    url(r'^categories/?$', utils.get_listview('stock', 'Category').as_view(), name="categories"),
    url(r'^categories/(?P<pk>[0-9]+)/?$', utils.get_listview('stock', 'Category').as_view(), name='category'),
    url(r'^stocks/?$', utils.get_listview('stock', 'Stock').as_view(), name="stocks"),
    url(r'^stocks/(?P<pk>[0-9]+)/?$', utils.get_listview('stock', 'Stock').as_view(), name='stock'),
    url(r'^stocklists/?$', utils.get_listview('stock', 'StockList').as_view(), name="stocklists"),
    url(r'^stocklists/(?P<pk>[0-9]+)/?$', utils.get_listview('stock', 'StockList').as_view(), name='stocklist'),
    url(r'^stocklistpositions/?$', utils.get_listview('stock', 'StockListPosition').as_view(), name="stocklistpositions"),
    url(r'^stocklistposition/(?P<pk>[0-9]+)/?$', utils.get_listview('stock', 'StockListPosition').as_view(), name='stocklistposition'),
    url(r'^stocktransfers/?$', utils.get_listview('stock', 'StockTransfer').as_view(), name="stocktransfers"),
    url(r'^stocktransfers/(?P<pk>[0-9]+)/?$', utils.get_listview('stock', 'StockTransfer').as_view(), name='stocktransfer'),
    url(r'^stockchanges/?$', utils.get_listview('stock', 'StockChange').as_view(), name="stockchanges"),
    url(r'^stockchange/(?P<pk>[0-9]+)/?$', utils.get_listview('stock', 'StockChange').as_view(), name='stockchange'),
]

transport = [
    url(r'^cars/?$', utils.get_listview('transport', 'Car').as_view(), name="cars"),
    url(r'^cars/(?P<pk>[0-9]+)/?$', utils.get_listview('transport', 'Car').as_view(), name='car'),
    url(r'^velostates/?$', utils.get_listview('transport', 'VeloState').as_view(), name="velostates"),
    url(r'^velostates/(?P<pk>[0-9]+)/?$', utils.get_listview('transport', 'VeloState').as_view(), name='velostate'),
    url(r'^rides/?$', utils.get_listview('transport', 'Ride').as_view(), name="rides"),
    url(r'^rides/(?P<pk>[0-9]+)/?$', utils.get_listview('transport', 'Ride').as_view(), name='ride'),
    url(r'^drivers/?$', utils.get_listview('transport', 'Driver').as_view(), name="drivers"),
    url(r'^drivers/(?P<pk>[0-9]+)/?$', utils.get_listview('transport', 'Driver').as_view(), name='driver'),
]

organisation = [
    url(r'^organisations/?$', views.OrganisationList.as_view(), name="organisations"),
    url(r'^organisations/(?P<pk>[0-9]+)/?$', views.OrganisationDetail.as_view(), name='organisations_detail'),

    url(r'^municipalities/?$', utils.get_listview('organisation', 'Municipality').as_view(), name="municipalities"),
    url(r'^municipalities/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('organisation', 'Municipality').as_view(), name='municipality'),
    url(r'^cantons/?$', utils.get_listview('organisation', 'Canton').as_view(), name="cantons"),
    url(r'^cantons/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('organisation', 'Canton').as_view(), name='canton'),
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
    url(r'^containers/?$', utils.get_listview('velafrica_sud', 'Container').as_view(), name="containers"),
    url(r'^containers/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('velafrica_sud', 'Container').as_view(), name='container'),
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
    url(r'^transport/', include(transport, namespace="transport")),
    url(r'^velafrica_sud/', include(velafrica_sud, namespace="velafrica_sud")),
    url(r'^counter/', include(counter, namespace="counter")),
    url(r'^collections/', include(collection, namespace="collections")),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
]

urlpatterns = format_suffix_patterns(urlpatterns)