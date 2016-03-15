# -*- coding: utf-8 -*-
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from velafrica.sbbtracking.models import Tracking, TrackingEvent


class TrackingEventInline(admin.TabularInline):
	model = TrackingEvent
	extra = 0


class TrackingAdmin(SimpleHistoryAdmin):
	inlines = [TrackingEventInline]


admin.site.register(Tracking, TrackingAdmin)
