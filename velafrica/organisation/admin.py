# -*- coding: utf-8 -*-
from django.contrib import admin
from velafrica.organisation.models import Organisation, Person
from simple_history.admin import SimpleHistoryAdmin

"""
class PartnerAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'description')
    search_fields = ['name', 'description']
"""

admin.site.register(Organisation)
admin.site.register(Person)
