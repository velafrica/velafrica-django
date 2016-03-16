# -*- coding: utf-8 -*-
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from velafrica.sbbtracking.models import Tracking, TrackingEvent, TrackingEventType, EmailLog


class TrackingEventInline(admin.TabularInline):
	model = TrackingEvent
	extra = 0

class EmailLogInline(admin.TabularInline):
	model = EmailLog
	fields = ('datetime', 'receiver', 'subject', 'message')
	readonly_fields = ('datetime', 'receiver', 'subject', 'message')
	extra = 0

	# do not allow users to create new email logs themselves
	def has_add_permission(self, request):
		return False


class TrackingAdmin(SimpleHistoryAdmin):
	inlines = [TrackingEventInline, EmailLogInline]


admin.site.register(Tracking, TrackingAdmin)
admin.site.register(TrackingEventType)
