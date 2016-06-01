# -*- coding: utf-8 -*-
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from velafrica.velafrica_sud.models import Country, Forwarder, PartnerSud, Container
from import_export import resources
from import_export.admin import ImportExportMixin

class ContainerResource(resources.ModelResource):
    """
    Define the Conainter resource for import / export.
    """

    class Meta:
        model = Container
        fields = ('container_no', 'container_no', 'organisation_from', 'organisation_from__name', 'partner_to', 'partner_to__name', 'velos_loaded', 'velos_unloaded', 'spare_parts', 'logistics', 'logistics__name', 'pickup_date', 'shipment_date', 'arrival_port_date', 'arrival_partner_date', 'velos_worth', 'spare_parts_worth', 'tools_worth', 'various_worth', 'seal_no', 'sgs_certified', 'notes')


class ContainerAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = ContainerResource
    list_display = ['pickup_date', 'container_no', 'organisation_from', 'partner_to', 'velos_loaded', 'velos_unloaded']
    search_fields = ['container_no', 'organisation_from__name', 'partner_to__name']
    list_filter = ['organisation_from', 'partner_to',]
    fieldsets = (
        (None, {
            'fields': ('container_no', 'organisation_from', 'partner_to', 'velos_loaded', 'velos_unloaded', 'spare_parts', )
            }),
        ('Transport', {
            'fields': ('logistics', 'pickup_date', 'shipment_date', 'arrival_port_date', 'arrival_partner_date')
            }),
        ('Worth', {
            'fields': ('velos_worth', 'spare_parts_worth', 'tools_worth', 'various_worth')
            }),
        ('Extra info', {
            'fields': ('seal_no', 'sgs_certified', 'notes')
            })
    )

class ContainerInline(admin.TabularInline):
    model = Container
    fields = ('pickup_date', 'container_no', 'organisation_from', 'velos_loaded', 'velos_unloaded')
    readonly_fields = ('pickup_date', 'container_no', 'organisation_from', 'velos_loaded', 'velos_unloaded')
    extra = 0

class PartnerSudAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'country', 'website', 'get_container_count', 'get_bicycle_count']
    search_fields = ['name', 'country__name']
    inlines = [ContainerInline]


admin.site.register(Container, ContainerAdmin)
admin.site.register(PartnerSud, PartnerSudAdmin)
admin.site.register(Country)
admin.site.register(Forwarder)
