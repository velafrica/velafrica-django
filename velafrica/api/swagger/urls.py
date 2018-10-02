# -*- coding: utf-8 -*-
from django.conf.urls import url

from velafrica.api.swagger import views

# where it all comes together
urlpatterns = [
    url(r'^$', views.schema_view),
]
