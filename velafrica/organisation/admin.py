from django.contrib import admin
from velafrica.partner.models import Partner
from simple_history.admin import SimpleHistoryAdmin

"""
class PartnerAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'description')
    search_fields = ['name', 'description']
"""

admin.site.register(Partner)
