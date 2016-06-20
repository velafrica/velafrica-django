# -*- coding: utf-8 -*-
from django_object_actions import DjangoObjectActions
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from velafrica.sbbtracking.models import Tracking
from velafrica.velafrica_sud.models import Country, Forwarder, PartnerSud, Container
from import_export import resources
from import_export.admin import ImportExportMixin

class TrackingInline(admin.TabularInline):
    """
    """
    model = Tracking
    extra = 0
    can_delete = False
    editable_fields = []
    fields = ['tracking_no', 'first_name', 'last_name', 'email', 'last_event']

    def get_readonly_fields(self, request, obj=None):
        fields = []
        for field in self.model._meta.get_all_field_names():
            if (not field == 'id'):
                if (field not in self.editable_fields):
                    fields.append(field)
        return fields
    
    def has_add_permission(self, request):
        return False

class ContainerResource(resources.ModelResource):
    """
    Define the Conainter resource for import / export.
    """

    class Meta:
        model = Container
        fields = ('container_no', 'container_no', 'organisation_from', 'organisation_from__name', 'partner_to', 'partner_to__name', 'velos_loaded', 'velos_unloaded', 'spare_parts', 'logistics', 'logistics__name', 'pickup_date', 'shipment_date', 'arrival_port_date', 'arrival_partner_date', 'velos_worth', 'spare_parts_worth', 'tools_worth', 'various_worth', 'seal_no', 'sgs_certified', 'notes')


class ContainerAdmin(ImportExportMixin, DjangoObjectActions, SimpleHistoryAdmin):
    resource_class = ContainerResource
    list_display = ['pickup_date', 'container_no', 'organisation_from', 'partner_to', 'velos_loaded', 'velos_unloaded', 'spare_parts']
    search_fields = ['container_no', 'organisation_from__name', 'partner_to__name']
    list_filter = ['organisation_from', 'partner_to',]
    change_actions = ('book_container',)
    inlines = [TrackingInline]
    fieldsets = (
        (None, {
            'fields': ('container_no', 'organisation_from', 'partner_to', 'velos_loaded', 'velos_unloaded', 'spare_parts', 'stocklist')
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

    def book_container(self, request, obj):
        """
        Admin action to book a container.
        """
        if obj:
            result = obj.book()
            print result
            if result:
                self.message_user(request, u"Container {} erfolgreich verbucht. {} von {} Trackings aktualisiert. ".format(obj.id, result[2], result[1]))
            else:
                self.message_user(request, "Container %s wurde bereits verbucht." % obj.id)
        else:
            self.message_user(request, "Not sure which Container to book." % obj.id)
        
    book_container.short_description = "Container Verbuchen"
    book_container.label = "Verbuchen"


class ContainerInline(admin.TabularInline):
    model = Container
    fields = ('pickup_date', 'container_no', 'organisation_from', 'velos_loaded', 'velos_unloaded')
    extra = 0

class PartnerSudAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'country', 'website', 'get_container_count', 'get_bicycle_count']
    search_fields = ['name', 'country__name']
    inlines = [ContainerInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'website', 'image' )
            }),
        ('Location', {
            'fields': ('street', 'zipcode', 'area', 'country', 'longitude', 'latitude')
            }),
        ('Organisation', {
            'fields': ('legalform', 'org_type', 'partner_since', )
            }),
    )


admin.site.register(Container, ContainerAdmin)
admin.site.register(PartnerSud, PartnerSudAdmin)
admin.site.register(Country)
admin.site.register(Forwarder)
