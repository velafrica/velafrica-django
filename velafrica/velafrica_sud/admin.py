# -*- coding: utf-8 -*-
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from velafrica.velafrica_sud.models import Country, Forwarder, PartnerSud, Container


class ContainerAdmin(SimpleHistoryAdmin):
    list_display = ['pickup_date', 'container_no', 'organisation_from', 'partner_to', 'velos_loaded', 'velos_unloaded']
    search_fields = ['container_no', 'organisation_from', 'partner_to']
    list_filter = ['organisation_from', 'partner_to',]
    fieldsets = (
        (None, {
            'fields': ('organisation_from', 'partner_to', 'velos_loaded', 'velos_unloaded', 'spare_parts', )
            }),
        ('Transport', {
            'fields': ('logistics', 'pickup_date', 'shipment_date', 'arrival_port_date', 'arrival_partner_date')
            }),
        ('Worth', {
            'fields': ('velos_worth', 'spare_parts_worth', 'tools_worth', 'various_worth')
            }),
        ('Extra info', {
            'fields': ('container_no', 'seal_no', 'sgs_certified', 'notes')
            })
    )


class PartnerSudAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'country']
    search_fields = ['name', 'country']


admin.site.register(Container, ContainerAdmin)
admin.site.register(PartnerSud, PartnerSudAdmin)
admin.site.register(Country)
admin.site.register(Forwarder)
