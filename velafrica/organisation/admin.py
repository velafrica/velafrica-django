# -*- coding: utf-8 -*-
from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django_object_actions import DjangoObjectActions
from import_export import resources
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin

from velafrica.organisation.models import Organisation, Person, Address, Country


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
    list_display = ['name', 'get_googlemaps_link', 'website', 'is_partnersud']
    search_fields = ['name', 'address__city']
    fields = ['name', 'website', 'facebook', 'get_partnersud', 'address', 'get_googlemaps_link', 'contact',
              'description']
    readonly_fields = ['get_partnersud', 'get_googlemaps_link']

    def get_googlemaps_link(self, obj):
        if obj.address:
            url = obj.address.get_googlemaps_url()
            if url:
                return mark_safe(u"<a href='{}' target='_blank'>{}</a>".format(
                    url,
                    obj.address
                ))
            else:
                return ""

    get_googlemaps_link.short_description = 'Google Maps'


class AddressAdmin(DjangoObjectActions, SimpleHistoryAdmin):
    """
    """
    list_display = ['__str__', 'street', 'zipcode', 'city', 'state', 'country', 'latitude', 'longitude',
                    'get_googlemaps_link']
    search_fields = ['street', 'zipcode', 'city', 'country__name']
    readonly_fields = ['get_googlemaps_link']
    list_filter = ['state', 'country']
    change_actions = ['get_geolocation']
    changelist_actions = ['get_geolocations']
    actions = ['get_geolocations']

    def get_geolocation(self, request, obj):
        if obj.get_geolocation():
            self.message_user(request,
                              u"GPS Koordinaten erfolgreich ermittelt und gespeichert! ({}, {})".format(obj.latitude,
                                                                                                        obj.longitude))
        else:
            self.message_user(request,
                              u"GPS Koordinaten konnten nicht ermittelt werden. Möglicherweise sind die Adressangaben nicht korrekt oder zu ungenau.",
                              level=messages.WARNING)

    get_geolocation.short_description = "GPS Koordinaten ermitteln"
    get_geolocation.label = "GPS Koordinaten ermitteln"

    def get_geolocations(self, request, queryset):
        count = 0
        for a in queryset:
            if not a.latitude:
                result = a.get_geolocation()
                if result:
                    count += 1
        if count > 0:
            self.message_user(request, u"GPS Koordinaten auf {} Adressen ermittelt und gespeichert".format(count))
        else:
            self.message_user(request,
                              u"GPS Koordinaten konnten nicht ermittelt werden. Möglicherweise sind die Adressangaben nicht korrekt oder zu ungenau.",
                              level=messages.WARNING)

    get_geolocations.short_description = "GPS Koordinaten ermitteln"
    get_geolocations.label = "GPS Koordinaten ermitteln"

    def get_googlemaps_link(self, obj):
        url = obj.get_googlemaps_url()
        if url:
            return mark_safe(u"<a href='{}' target='_blank'>{}</a>".format(
                url,
                "Google Maps"
            ))
        else:
            return ""

    get_googlemaps_link.short_description = 'Google Maps'


class CountryAdmin(SimpleHistoryAdmin):
    """
    """
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Country, CountryAdmin)
