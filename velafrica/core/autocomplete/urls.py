# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import path

from velafrica.stock import views as stock_views
from velafrica.transport import views as transport_views

app_name = "autocomplete"

urlpatterns = [
    # autocomplete urls
    url(r'^product/$', stock_views.ProductAutocomplete.as_view(), name='product'),
    url(r'^warehouse/$', stock_views.WarehouseAutocomplete.as_view(), name='warehouse'),
    url(r'^driver/$', transport_views.DriverAutocomplete.as_view(), name='driver'),
    path('car/', transport_views.CarAutocomplete.as_view(), name='car'),
    path('request_category/', transport_views.RequestCategoryAutocomplete.as_view(), name='request_category'),
    path('velostate/', transport_views.VeloStateAutocomplete.as_view(), name='velostate'),
]
