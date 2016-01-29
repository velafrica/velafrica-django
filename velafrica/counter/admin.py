from django.contrib import admin
from velafrica.counter.models import Entry
from import_export import resources
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin

class EntryResource(resources.ModelResource):
    """
    Define the resource for counter entry.
    """

    class Meta:
        model = Entry

class EntryAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = EntryResource
    list_display = ('date', 'organisation', 'amount', 'note')
    search_fields = ['note', 'organisation']
    list_editable = ['amount', 'note']
    list_filter = ['date', 'organisation', 'amount']

admin.site.register(Entry, EntryAdmin)