# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export import fields, resources, widgets
from import_export.admin import ImportExportMixin, ExportMixin, ImportMixin
from simple_history.admin import SimpleHistoryAdmin

from velafrica.collection.models import *


class TaskProgressInline(admin.TabularInline):
    model = TaskProgress
    fields = ('task', 'notes', 'status')
    extra = 0


class TaskProgressResource(resources.ModelResource):
    """
    Define the collection event resource for import / export.
    """

    class Meta:
        model = TaskProgress
        fields = [
            'task',
            'task__name',
            'notes',
            'status',
            'collection_event',
            'collection_event__event__name',
        ]

class TaskProgressAdmin(ExportMixin, SimpleHistoryAdmin):
    resource_class = TaskProgressResource
    list_filter = ['status']
    list_display = ['__unicode__', 'collection_event', 'task', 'notes', 'status']


class EventAdmin(SimpleHistoryAdmin):
    list_filter = ['yearly']
    list_display = ['name', 'yearly']

class CollectionEventAdminResource(resources.ModelResource):
    """
    Define the collection event resource for import / export.
    """

    marketing_status = fields.Field()
    transport_status = fields.Field()
    feedback_status = fields.Field()

    def dehydrate_marketing_status(self, book):
        return book.get_status_marketing()

    def dehydrate_transport_status(self, book):
        return book.get_status_logistics()

    def dehydrate_feedback_status(self, book):
        return book.get_status_results()

    class Meta:
        model = CollectionEvent
        fields = [
            'date_start',
            'date_end',
            'event',
            'event__name',
            'event__region__name',
            'time',
            'notes',
            'presence_velafrica',
            'presence_velafrica_info',
            'collection',
            'collection_partner_vrn',
            'collection_partner_vrn__name',
            'collection_partner_other',
            'collection_partner_confirmed',
            'intermediate_store',
            'processing',
            'processing__name',
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
            'event__address_notes',
            'marketing_status',
            'transport_status',
            'feedback_status',
            'complete'
        ]


class CollectionEventAdmin(ImportExportMixin, SimpleHistoryAdmin):
    """
    """
    resource_class = CollectionEventAdminResource
    list_display = ['date_start', 'date_end', 'event', 'status_logistics', 'status_marketing', 'status_results', 'velo_amount', 'complete', 'notes' ]
    search_fields = ['event__name', 'event__address__city']

    inlines = [TaskProgressInline]
    readonly_fields = ['get_googlemaps_link', 'get_event_name', 'get_event_description', 'get_event_region', 'get_event_category', 'get_event_yearly', 'get_event_host', 'get_event_host_type', 'get_event_address', 'get_event_address_notes']
    fieldsets = (
        ('Sammelanlass', {
            'fields': ('date_start', 'date_end', 'event', 'time', 'notes', 'complete' )
            }),
        ('Event', {
            'fields': ('get_event_description', 'get_event_category', 'get_event_region', 'get_event_yearly', 'get_event_host', 'get_event_host_type', 'get_googlemaps_link', 'get_event_address_notes')
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
    list_filter = ['complete', 'date_start', 'event']

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
    status_marketing.short_description = 'Marketing'

    def status_results(self, obj):
        return mark_safe('<div span style="{}">&nbsp;</div>'.format(self.get_status_style(obj.get_status_results())))
    status_results.short_description = 'Feedback'

    def status_logistics(self, obj):
        return mark_safe('<div span style="{}">&nbsp;</div>'.format(self.get_status_style(obj.get_status_logistics())))
    status_logistics.short_description = 'Abholung'


class DropoffResource(resources.ModelResource):
    """
    Define the Dropoff resource for import / export
    """

    class Meta:
        model = Dropoff


class DropoffAdmin(ImportExportMixin, admin.ModelAdmin):
    resources_class = DropoffResource
    search_fields = ['name', 'address__street', 'address__zipcode', 'address__city']
    list_filter = ['active', 'sbb', 'temp', 'pickup']
    fieldsets = (
        ('Allgemein', {
            'fields': ('name', 'active', 'sbb', 'address', 'contact_person',
                       'phone_number', 'opening_time', 'notes')
        }),
        ('Temporäre Abgabestelle', {
            'fields': ('temp', 'temp_start', 'temp_end',)
        }),
        ('Abholservice', {
            'fields': ('pickup', 'pickup_description',)
        }),
        ('Benutzerdefinierter Pin auf Karte', {
            'fields': ('custom_lat', 'custom_lon'),
        }),
    )


admin.site.register(Dropoff, DropoffAdmin)
admin.site.register(Region)
admin.site.register(Event, EventAdmin)
admin.site.register(EventCategory)
admin.site.register(HostType)
admin.site.register(CollectionEvent, CollectionEventAdmin)
admin.site.register(Task)
admin.site.register(TaskProgress,TaskProgressAdmin)
