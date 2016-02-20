# -*- coding: utf-8 -*-
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from velafrica.velafrica_sud.models import Country, PartnerSud, Container


class ContainerAdmin(SimpleHistoryAdmin):
    list_display = ['container_no', 'pickup_date', 'organisation_from', 'partner_to', 'velos']
    search_fields = ['container_no', 'organisation_from', 'partner_to']


class PartnerSudAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'country']
    search_fields = ['name', 'country']


admin.site.register(Container, ContainerAdmin)
admin.site.register(PartnerSud, PartnerSudAdmin)
admin.site.register(Country)
