# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns

from velafrica.api import utils
from velafrica.api import views
from velafrica.api import views_public
from velafrica.api.collections import views as views_collections
from velafrica.api.counter.views import CounterEntryList, CounterEntryDetail
from velafrica.api.organisation.views import OrganisationDetail, OrganisationList
from velafrica.api.sbbtracking.views import TrackingList, TrackingEventList
from velafrica.api.stock import views as views_stock
from velafrica.api.user import views as views_user
from velafrica.api.velafrica_sud import views as views_velafrica_sud

app_name = "api"

collection = [
    url(r'^eventcategories/?$', utils.get_listview('collection', 'EventCategory').as_view(), name="eventcategories"),
    url(r'^eventcategories/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('collection', 'EventCategory').as_view(),
        name='eventcategory'),
    url(r'^events/?$', utils.get_listview('collection', 'Event').as_view(), name="events"),
    url(r'^events/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('collection', 'Event').as_view(), name='event'),
    url(r'^dropoffs/?$', utils.get_listview('collection', 'Dropoff').as_view(), name="dropoffs"),
    url(r'^dropoffs/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('collection', 'Dropoff').as_view(), name='dropoffs'),
    url(r'^tasks/?$', utils.get_listview('collection', 'Task').as_view(), name="tasks"),
    url(r'^tasks/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('collection', 'Task').as_view(), name='tasks'),
    url(r'^taskprogresses/?$', utils.get_listview('collection', 'TaskProgress').as_view(), name="tasksprogresses"),
    url(r'^taskprogresses/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('collection', 'TaskProgress').as_view(),
        name='taskprogress'),
    url(r'^collectionevents/?$', utils.get_listview('collection', 'CollectionEvent').as_view(),
        name="collectionevents"),
    url(r'^collectionevents/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('collection', 'CollectionEvent').as_view(),
        name='collectionevent'),
    url(r'^hosttypes/?$', utils.get_listview('collection', 'HostType').as_view(), name="hosttypes"),
    url(r'^hosttypes/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('collection', 'HostType').as_view(), name='hosttypes'),
]

counter = [
    url(r'^entries/?$', CounterEntryList.as_view(), name="entries"),
    url(r'^entries/(?P<pk>[0-9]+)/?$', CounterEntryDetail.as_view(), name='entry'),
]

stock = [
    url(r'^warehouses/?$', utils.get_listview('stock', 'Warehouse').as_view(), name="warehouses"),
    url(r'^warehouses/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('stock', 'Warehouse').as_view(), name='warehouse'),
    url(r'^products/?$', utils.get_listview('stock', 'Product').as_view(), name="products"),
    url(r'^products/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('stock', 'Product').as_view(), name='product'),
    url(r'^categories/?$', utils.get_listview('stock', 'Category').as_view(), name="categories"),
    url(r'^categories/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('stock', 'Category').as_view(), name='category'),
    url(r'^stocks/?$', utils.get_listview('stock', 'Stock').as_view(), name="stocks"),
    url(r'^stocks/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('stock', 'Stock').as_view(), name='stock'),
    url(r'^stocklists/?$', utils.get_listview('stock', 'StockList').as_view(), name="stocklists"),
    url(r'^stocklists/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('stock', 'StockList').as_view(), name='stocklist'),
    url(r'^stocklistpositions/?$', utils.get_listview('stock', 'StockListPosition').as_view(),
        name="stocklistpositions"),
    url(r'^stocklistposition/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('stock', 'StockListPosition').as_view(),
        name='stocklistposition'),

    url(r'^stocktransfers/?$', utils.get_listview('stock', 'StockTransfer').as_view(), name="stocktransfers"),
    url(r'^stocktransfers/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('stock', 'StockTransfer').as_view(),
        name='stocktransfer'),
    url(r'^stocktransfers/(?P<pk>[0-9]+)/book$', views_stock.book, name='stocktransfer'),
    # url(r'^stocktransfers/(?P<pk>[0-9]+)/revoke$', utils.get_retrieveview('stock', 'StockTransfer').as_view(), name='stocktransfer'),

    url(r'^stockchanges/?$', utils.get_listview('stock', 'StockChange').as_view(), name="stockchanges"),
    url(r'^stockchange/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('stock', 'StockChange').as_view(),
        name='stockchange'),
]

transport = [
    url(r'^cars/?$', utils.get_listview('transport', 'Car').as_view(), name="cars"),
    url(r'^cars/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('transport', 'Car').as_view(), name='car'),
    url(r'^velostates/?$', utils.get_listview('transport', 'VeloState').as_view(), name="velostates"),
    url(r'^velostates/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('transport', 'VeloState').as_view(), name='velostate'),
    url(r'^rides/?$', utils.get_listview('transport', 'Ride').as_view(), name="rides"),
    url(r'^rides/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('transport', 'Ride').as_view(), name='ride'),
    url(r'^drivers/?$', utils.get_listview('transport', 'Driver').as_view(), name="drivers"),
    url(r'^drivers/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('transport', 'Driver').as_view(), name='driver'),
]

organisation = [
    url(r'^organisations/?$', OrganisationList.as_view(), name="organisations"),
    url(r'^organisations/(?P<pk>[0-9]+)/?$', OrganisationDetail.as_view(), name='organisations_detail'),
    url(r'^countries/?$', utils.get_listview('organisation', 'Country').as_view(), name='countries'),
    url(r'^countries/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('organisation', 'Country').as_view(), name='country'),
]

tracking = [
    url(r'^trackings/?$', TrackingList.as_view(), name="trackings"),
    url(r'^trackings/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('sbbtracking', 'Tracking').as_view(), name='tracking'),
    url(r'^trackingevents/?$', TrackingEventList.as_view(), name="trackingevents"),
    url(r'^trackingevents/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('sbbtracking', 'TrackingEvent').as_view(),
        name='trackingevent'),
    url(r'^trackingeventtypes/?$', utils.get_listview('sbbtracking', 'TrackingEventType').as_view(),
        name="trackingeventtypes"),
    url(r'^trackingeventtypes/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('sbbtracking', 'TrackingEventType').as_view(),
        name='trackingeventtype'),
    url(r'^velotypes/?$', utils.get_listview('sbbtracking', 'VeloType').as_view(), name="velotypes"),
    url(r'^velotypes/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('sbbtracking', 'VeloType').as_view(), name='velotype'),
]

# first attempt at generic views
velafrica_sud = [
    url(r'^containers/?$', views_velafrica_sud.ContainerList.as_view(), name="containers"),
    url(r'^containers/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('velafrica_sud', 'Container').as_view(),
        name='container'),
    url(r'^forwarders/?$', utils.get_listview('velafrica_sud', 'Forwarder').as_view(), name="forwarders"),
    url(r'^forwarders/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('velafrica_sud', 'Forwarder').as_view(),
        name='forwarder'),
    url(r'^partners/?$', utils.get_listview('velafrica_sud', 'PartnerSud').as_view(), name="partners"),
    url(r'^partners/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('velafrica_sud', 'PartnerSud').as_view(),
        name='partner'),
    url(r'^reports/?$', utils.get_listview('velafrica_sud', 'Report').as_view(), name="reports"),
    url(r'^reports/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('velafrica_sud', 'Report').as_view(), name='report'),
]

bikes = [
    url(r'^bikes/?$', utils.get_listview('bikes', 'Bike').as_view(), name="bikes"),
    url(r'^bikes/(?P<pk>[0-9]+)/?$', utils.get_retrieveview('bikes', 'Bike').as_view(),
        name='container'),
]

public = [
    url(r'^dropoffs/$', views_public.get_dropoffs, name="dropoffs"),
    url(r'^collectionevents/$', views_collections.CollectionEventListPublic.as_view(), name="collectionevents-public"),
    url(r'^subscribe-newsletter/$', views_public.subscribe_newsletter, name="subscribe-newsletter"),
]

user = [
    url(r'^current/$', views_user.current_user, name="current_user"),

]

# where it all comes together
urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^swagger/', include('velafrica.api.swagger.urls')),

    url(r'^user/', include((user, app_name))),

    url(r'^organisation/', include((organisation, app_name), namespace='organisation')),
    url(r'^stock/', include((stock, app_name))),
    url(r'^bikes/', include((bikes, app_name))),
    url(r'^tracking/', include((tracking, app_name))),
    url(r'^transport/', include((transport, app_name))),
    url(r'^velafrica_sud/', include((velafrica_sud, app_name))),
    url(r'^counter/', include('velafrica.api.counter.urls')),
    url(r'^collections/', include((collection, app_name))),
    url(r'^public/', include((public, app_name), namespace='public'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
