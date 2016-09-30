from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from velafrica.download.models import File


class FileAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'description')
    search_fields = ['name', 'description']

admin.site.register(File, FileAdmin)
