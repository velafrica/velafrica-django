from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.fields import Field
from import_export.widgets import DateWidget
from simple_history.admin import SimpleHistoryAdmin
from velafrica.collection.models import *
from velafrica.collection.forms import CollectionEventForm


class TaskProgressInline(admin.TabularInline):
    model = TaskProgress
    fields = ('task', 'notes', 'status')
    extra = 0


class CollectionEventAdmin(SimpleHistoryAdmin):
    """
    """
    form = CollectionEventForm
    list_display = ['date_start', 'event', 'municipality_name' 'notes', 'get_task_progress_summary_string', 'velo_amount' ]
    search_fields = ['municipality_name', 'event__name']
    inlines = [TaskProgressInline]


admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(CollectionEvent, CollectionEventAdmin)
admin.site.register(Task)
admin.site.register(TaskProgress)