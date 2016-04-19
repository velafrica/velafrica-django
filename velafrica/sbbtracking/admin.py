# -*- coding: utf-8 -*-
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from velafrica.sbbtracking.models import Tracking, TrackingEvent, TrackingEventType, EmailLog
from import_export import resources
from import_export.admin import ImportExportMixin


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

class TrackingResource(resources.ModelResource):
    """
    Define the Tracking resource for import / export.
    """

    class Meta:
        model = Tracking
        import_id_fields = ('tracking_no',)
        fields = ('first_name', 'last_name', 'email', 'tracking_no', 'number_of_velos')

class TrackingAdmin(ImportExportMixin, SimpleHistoryAdmin):
	resource_class = TrackingResource
	list_display = ('tracking_no', 'first_name', 'last_name', 'number_of_velos', 'get_last_event')
	inlines = [TrackingEventInline, EmailLogInline]


class TrackingEventTypeAdmin(SimpleHistoryAdmin):
	list_display = ('name', 'description', 'send_email')


admin.site.register(Tracking, TrackingAdmin)
admin.site.register(TrackingEventType, TrackingEventTypeAdmin)
