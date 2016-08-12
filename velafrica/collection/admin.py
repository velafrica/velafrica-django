# -*- coding: utf-8 -*-
from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.fields import Field
from import_export.widgets import DateWidget
from simple_history.admin import SimpleHistoryAdmin
from velafrica.collection.models import *
from velafrica.collection.forms import EventForm


class TaskProgressInline(admin.TabularInline):
    model = TaskProgress
    fields = ('task', 'notes', 'status')
    extra = 0


class EventAdmin(SimpleHistoryAdmin):
    form = EventForm
    list_filter = ['yearly']

class CollectionEventAdminResource(resources.ModelResource):
    """
    Define the collection event resource for import / export.
    """

    class Meta:
        model = CollectionEvent
        fields = [
            'date_start',
            'date_end',
            'event',
            'event__name',
            'time',
            'notes',
            'presence_velafrica',
            'presence_velafrica_info',
            'collection',
            'collection_partner_vrn',
            'collection_partner_vrn__name',
            'collection_partner_other',
            'collection_partner_confirmed',
            'processing',
            'processing_notes',
            'website',
            'feedback',
            'velo_amount',
            'people_amount',
            'hours_amount',
            'additional_results',
            'event__description', 
            'event__category__name',
            'event__yearly',
            'event__host',
            'event__host_type__name',
            'event__address__street',
            'event__address__city',
            'event__address__zipcode',
            'event__address_notes'
        ]

class CollectionEventAdmin(ImportExportMixin, SimpleHistoryAdmin):
    """
    """
    resource_class = CollectionEventAdminResource
    list_display = ['date_start', 'date_end', 'event', 'notes', 'status_logistics', 'status_marketing', 'status_results', 'velo_amount' ]
    search_fields = ['event__name', 'event__address__city']

    inlines = [TaskProgressInline]
    readonly_fields = ['get_googlemaps_link', 'get_event_name', 'get_event_description', 'get_event_category', 'get_event_yearly', 'get_event_host', 'get_event_host_type', 'get_event_address', 'get_event_address_notes']
    fieldsets = (
        ('Sammelanlass', {
            'fields': ('date_start', 'date_end', 'event', 'time', 'notes')
            }),
        ('Event', {
            'fields': ('get_event_name', 'get_event_description', 'get_event_category', 'get_event_yearly', 'get_event_host', 'get_event_host_type', 'get_googlemaps_link', 'get_event_address_notes')
            }),
        ('Logistik', {
            'fields': ('presence_velafrica', 'presence_velafrica_info', 'collection_partner_vrn', 'collection_partner_other', 'collection_partner_confirmed', 'collection', 'processing', 'processing_notes',)
            }),
        ('Marketing', {
            'fields': ('website',)
            }),
        ('Resultate', {
            'fields': ('feedback', 'velo_amount', 'people_amount', 'hours_amount', 'additional_results')
            }),
    )
    list_filter = ['date_start', 'event']
    def get_googlemaps_link(self, obj):
        if obj.event.address:
            url = obj.address.event.get_googlemaps_url()
            if url:
                return mark_safe(u"<a href='{}' target='_blank'>{}</a>".format(
                    url,
                    obj.event.address
                ))
            else:
                return ""
    get_googlemaps_link.short_description = 'Google Maps'

    def get_status_style(self, status):
        """
        Helper function to get css styles in regards to task status.
        """
        print "get status style"
        style = "border-radius: 50%; width: 20px; height: 20px;"
        if status == "success":
            style += " background-color: #4DFA90;"
        elif status == "warning":
            style += " background-color: #FABE4D;"
        else:
            style += " background-color: #FF5468;"

        print style
        return style

    def status_marketing(self, obj):
        return mark_safe('<div span style="{}">&nbsp;</div>'.format(self.get_status_style(obj.get_status_marketing())))
    status_marketing.short_description = 'Marketing Status'

    def status_results(self, obj):
        return mark_safe('<div span style="{}">&nbsp;</div>'.format(self.get_status_style(obj.get_status_results())))
    status_results.short_description = 'Feedback Status'

    def status_logistics(self, obj):
        return mark_safe('<div span style="{}">&nbsp;</div>'.format(self.get_status_style(obj.get_status_logistics())))
    status_logistics.short_description = 'Abholung Status'

admin.site.register(Event, EventAdmin)
admin.site.register(EventCategory)
admin.site.register(HostType)
admin.site.register(CollectionEvent, CollectionEventAdmin)
admin.site.register(Task)
admin.site.register(TaskProgress)