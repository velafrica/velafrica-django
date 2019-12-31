# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import *
from django.urls import path

from velafrica.core import views
from velafrica.public_site import views as velafrica_public_site_views
from velafrica.stock import views as stock_views
from velafrica.transport import views as transport_views

app_name = "autocomplete"

urlpatterns = [
    # autocomplete urls
    url(r'^product/$', stock_views.ProductAutocomplete.as_view(), name='product'),
    url(r'^warehouse/$', stock_views.WarehouseAutocomplete.as_view(), name='warehouse'),
    url(r'^driver/$', transport_views.DriverAutocomplete.as_view(), name='driver'),
    path('car/', transport_views.CarAutocomplete.as_view(), name='car'),
]
