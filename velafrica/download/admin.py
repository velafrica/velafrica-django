from django.contrib import admin
from velafrica.download.models import File
from import_export import resources
from simple_history.admin import SimpleHistoryAdmin


class FileAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'description')
    search_fields = ['name', 'description']

admin.site.register(File, FileAdmin)
