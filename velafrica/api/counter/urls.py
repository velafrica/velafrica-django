# -*- coding: utf-8 -*-
from django.conf.urls import url

from velafrica.api.counter.views import CounterEntryList, CounterEntryDetail

urlpatterns = [
    url(r'^entries/?$', CounterEntryList.as_view(), name="entries"),
    url(r'^entries/(?P<pk>[0-9]+)/?$', CounterEntryDetail.as_view(), name='entry'),
]
