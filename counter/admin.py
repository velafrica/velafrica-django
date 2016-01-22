from django.contrib import admin
from counter.models import Entry
from simple_history.admin import SimpleHistoryAdmin

class EntryAdmin(SimpleHistoryAdmin):
    list_display = ('date', 'amount', 'note')
    search_fields = ['note']
    list_filter = ['date', 'amount']

admin.site.register(Entry, EntryAdmin)