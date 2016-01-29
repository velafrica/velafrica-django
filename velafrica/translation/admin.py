from django.contrib import admin
from velafrica.translation.models import Language
from simple_history.admin import SimpleHistoryAdmin

class LanguageAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'short')
    search_fields = ['name', 'short']

admin.site.register(Language, LanguageAdmin)