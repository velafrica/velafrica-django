from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from velafrica.collection.models import *
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.fields import Field
from import_export.widgets import DateWidget
from simple_history.admin import SimpleHistoryAdmin


class TaskProgressInline(admin.TabularInline):
    model = TaskProgress
    fields = ('task', 'notes', 'status')
    extra = 0


class EventAdmin(SimpleHistoryAdmin):
    """
    """
    list_display = ['date_start', 'municipality', 'collection_partner', 'notes', 'get_task_progress_summary_string', 'velo_amount' ]
    search_fields = ['municipality_name', 'collection_partner']
    inlines = [TaskProgressInline]
    fieldsets = (
        ('Eckdaten', {
            'fields': ('date_start', 'date_end', 'municipality', 'type', 'time', 'notes')
            }),
        ('Logistik', {
            'fields': ('presence_velafrica', 'pickup', 'processing', 'collection_partner', 'collection_type')
            }),
        ('Marketing', {
            'fields': ('website',)
            }),
        ('Resultate', {
            'fields': ('velo_amount', 'people_amount', 'hours_amount', 'additional_results')
            }),
    )

admin.site.register(Event, EventAdmin)
admin.site.register(EventType)
admin.site.register(CollectionPartner)
admin.site.register(Task)
admin.site.register(TaskStatus)
admin.site.register(TaskProgress)