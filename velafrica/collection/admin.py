# -*- coding: utf-8 -*-
from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
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

class CollectionEventAdminResource(resources.ModelResource):
    """
    Define the collection event resource for import / export.
    """

    class Meta:
        model = CollectionEvent

class CollectionEventAdmin(ImportExportMixin, SimpleHistoryAdmin):
    """
    """
    list_display = ['date_start', 'event', 'notes', 'get_status_logistics', 'get_status_marketing', 'get_status_results', 'velo_amount' ]
    search_fields = ['event__name', 'event__municipality__name']
    inlines = [TaskProgressInline]
    fieldsets = (
        ('Event', {
            'fields': ('date_start', 'date_end', 'event', 'time', 'notes')
            }),
        ('Logistik', {
            'fields': ('presence_velafrica', 'presence_velafrica_info', 'collection_partner_vrn', 'collection_partner_other', 'collection_partner_confirmed', 'pickup', 'processing', )
            }),
        ('Marketing', {
            'fields': ('website',)
            }),
        ('Resultate', {
            'fields': ('feedback', 'velo_amount', 'people_amount', 'hours_amount', 'additional_results')
            }),
    )


admin.site.register(Event, EventAdmin)
admin.site.register(EventCategory)
admin.site.register(CollectionEvent, CollectionEventAdmin)
admin.site.register(Task)
admin.site.register(TaskProgress)