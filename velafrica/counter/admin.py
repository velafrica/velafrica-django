from django.contrib import admin
from velafrica.counter.models import Entry
from simple_history.admin import SimpleHistoryAdmin

class EntryAdmin(SimpleHistoryAdmin):
    list_display = ('date', 'organisation', 'amount', 'note')
    search_fields = ['note', 'organisation']
    list_editable = ['amount', 'note']
    list_filter = ['date', 'organisation', 'amount']

admin.site.register(Entry, EntryAdmin)