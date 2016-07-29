# -*- coding: utf-8 -*-
from django.contrib import admin
from velafrica.organisation.models import Organisation, Person, Canton, Municipality, Address
from velafrica.stock.models import Warehouse
from import_export import resources
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from velafrica.velafrica_sud.models import PartnerSud

class PartnerSudInline(admin.StackedInline):
    model = PartnerSud

class PersonAdmin(SimpleHistoryAdmin):
    """
    """
    list_display = ['__str__', 'user', 'organisation']
    list_filter = ['organisation']
    search_fields = ['organisation__name', 'user__username']


class OrganisationResource(resources.ModelResource):
    """
    Define the organisation resource for import / export.
    """

    class Meta:
        model = Organisation


class OrganisationAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = OrganisationResource
    # inlines = [WarehouseInline,]
    list_display = ['name', 'street', 'plz', 'city', 'website', 'has_partnersud']
    search_fields = ['name', 'city']
    readonly_fields = ['street', 'plz', 'city']
    inlines = [PartnerSudInline]


class CantonResource(resources.ModelResource):
    """
    Define the organisation resource for import / export.
    """

    class Meta:
        model = Canton
        import_id_fields = ['short',]

class CantonAdmin(ImportExportMixin, SimpleHistoryAdmin):
    """
    """
    resource_class = CantonResource
    list_display = ['short', 'name']
    search_fields = ['short', 'name']


class MunicipalityResource(resources.ModelResource):
    """
    Define the organisation resource for import / export.
    """
    canton = Field(
            column_name='canton',
            attribute='canton',
            widget=ForeignKeyWidget(Canton, 'short'))
    
    class Meta:
        model = Municipality
        import_id_fields = ['gdenr', 'plz', 'name']
        fields = ['gdenr', 'name', 'name_short', 'plz', 'plz_name', 'canton']


class MunicipalityAdmin(ImportExportMixin, SimpleHistoryAdmin):
    """
    """
    resource_class = MunicipalityResource
    list_display = ['plz', 'plz_name', 'canton']
    search_fields = ['plz', 'plz_name', 'canton__name']
    list_filter = ['canton__name']


class AddressAdmin(SimpleHistoryAdmin):
    """
    """
    list_display = ['street', 'zipcode', 'city', 'state', 'country', 'longitude', 'latitude']
    search_fields = ['street', 'zipcode', 'city', 'country']
    list_filter = ['state', 'country']

admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Canton, CantonAdmin)
admin.site.register(Address, AddressAdmin)