# -*- coding: utf-8 -*-
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from velafrica.sbbtracking.models import Tracking, TrackingEventState, TrackingEvent

admin.site.register(Tracking)
admin.site.register(TrackingEventState)
admin.site.register(TrackingEvent)