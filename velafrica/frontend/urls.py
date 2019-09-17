from django.conf.urls import url
from django.views.generic import RedirectView, ListView

from velafrica.bikes.models import Bike
from velafrica.collection import views as collection_views
from velafrica.counter import views as counter_views
from velafrica.download import views as download_views
from velafrica.sbbtracking import views as sbbtracking_views
from velafrica.stock import views as stock_views
from velafrica.transport import views as transport_views
from velafrica.velafrica_sud import views as velafrica_sud_views

app_name="frontend"

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/velo_tracking')),
    url(r'^counter', counter_views.counter, name='counter'),
    url(r'^download', download_views.downloads, name='download'),
    url(r'^stock', stock_views.stock, name='stock'),
    url(r'^velo_tracking/(?P<tracking_no>\w+)', sbbtracking_views.tracking, name='tracking_detail'),
    url(r'^velo_tracking', sbbtracking_views.tracking, name='tracking'),
    url(r'^transport', transport_views.transport, name='transport'),
    url(r'^warehouses', stock_views.warehouses, name='warehouses'),
    url(r'^warehouse/(?P<pk>[0-9]+)', stock_views.warehouse, name='warehouse_detail'),
    url(r'^container', velafrica_sud_views.container, name='container'),
    url(r'^bikes', ListView.as_view(model=Bike), name='bike'),
    url(r'^collection', collection_views.collection, name='collection'),
]
