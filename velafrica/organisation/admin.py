# -*- coding: utf-8 -*-
from django.contrib import admin, messages
from django_object_actions import DjangoObjectActions
from velafrica.organisation.models import Organisation, Person, Canton, Municipality, Address, Country
from velafrica.stock.models import Warehouse
from import_export import resources
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from velafrica.velafrica_sud.models import PartnerSud


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
    list_display = ['name', 'address', 'website', 'is_partnersud']
    search_fields = ['name', 'address__city']
    fields = ['name', 'website', 'get_partnersud', 'address', 'contact','description']
    readonly_fields = ['get_partnersud']


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


class AddressAdmin(DjangoObjectActions, SimpleHistoryAdmin):
    """
    """
    list_display = ['__str__', 'street', 'zipcode', 'city', 'state', 'country', 'longitude', 'latitude']
    search_fields = ['street', 'zipcode', 'city', 'country']
    list_filter = ['state', 'country']
    change_actions = ['get_geolocation']
    changelist_actions = ['get_geolocations']

    def get_geolocation(self, request, obj):
        if obj.get_geolocation():
            self.message_user(request, "GeoLocation found and set!")
        else:
            self.message_user(request, "Could not find GeoLocation.", level=messages.WARNING)

    def get_geolocations(self, request, queryset):
        count = 0
        for a in queryset:
            if not a.latitude:
                result = a.get_geolocation()
                if result:
                    count += 1
        self.message_user(request, "GeoLocation set on {} addresses".format(count))



class CountryAdmin(SimpleHistoryAdmin):
    """
    """
    list_display = ['name', 'code']
    search_fields = ['name', 'code']

admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Canton, CantonAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Country, CountryAdmin)