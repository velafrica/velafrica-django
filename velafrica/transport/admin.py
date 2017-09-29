# -*- coding: utf-8 -*-
from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django_object_actions import DjangoObjectActions
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.fields import Field
from import_export.widgets import DateWidget, ForeignKeyWidget
from simple_history.admin import SimpleHistoryAdmin

from velafrica.organisation.models import Organisation
from velafrica.stock.models import Warehouse
from velafrica.transport.forms import RideForm
from velafrica.transport.models import Car, Driver, VeloState, Ride


class CarAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'organisation', 'plate']
    search_fields = ['name']

    def get_queryset(self, request):
        qs = super(CarAdmin, self).get_queryset(request)
        # superusers should see all entries
        if request.user.is_superuser:
            return qs
        # other users with a correlating person should only see their organisations entries
        elif hasattr(request.user, 'person'):
            return qs.filter(organisation=request.user.person.organisation)
        # users with no superuser role and no related person should not see any entries
        else:
            return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'organisation':
            if request.user.is_superuser:
                pass
            # other users with a correlating person should only see their organisation
            elif hasattr(request.user, 'person'):
                kwargs["queryset"] = Organisation.objects.filter(id=request.user.person.organisation.id)
            # users with no superuser role and no related person should not see any organisations
            else:
                kwargs["queryset"] = Organisation.objects.none()
        return super(CarAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class DriverAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'active', 'organisation']
    search_fields = ['name', 'organisation']
    list_filter = ['active']

    def get_queryset(self, request):
        qs = super(DriverAdmin, self).get_queryset(request)
        # superusers should see all entries
        if request.user.is_superuser:
            return qs
        # other users with a correlating person should only see their organisations entries
        elif hasattr(request.user, 'person'):
            return qs.filter(organisation=request.user.person.organisation)
        # users with no superuser role and no related person should not see any entries
        else:
            return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'organisation':
            if request.user.is_superuser:
                pass
            # other users with a correlating person should only see their organisation
            elif hasattr(request.user, 'person'):
                kwargs["queryset"] = Organisation.objects.filter(id=request.user.person.organisation.id)
            # users with no superuser role and no related person should not see any organisations
            else:
                kwargs["queryset"] = Organisation.objects.none()
        return super(DriverAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class VeloStateAdmin(SimpleHistoryAdmin):
    list_display = ['name']
    search_fields = ['name']


class RideResource(resources.ModelResource):
    """
    Define the ride resource for import / export.
    """
    from_warehouse = Field(
        column_name='from_warehouse',
        attribute='from_warehouse',
        widget=ForeignKeyWidget(Warehouse, 'id'))

    date = Field(
        column_name='date',
        attribute='date',
        widget=DateWidget(format="%d.%m.%Y"))

    def get_instance(self, instance_loader, row):
        """
        Don't check for existing data rows.
        """
        return False

    class Meta:
        model = Ride
        fields = ('date', 'from_warehouse', 'from_warehouse__name', 'to_warehouse', 'to_warehouse__name', 'driver', 'driver__name', 'car', 'car__name', 'velos', 'velo_state', 'velo_state__name', 'spare_parts', )


class RideAdmin(ImportExportMixin, DjangoObjectActions, SimpleHistoryAdmin):
    form = RideForm
    resource_class = RideResource
    list_display = ['id', 'date', 'from_warehouse', 'to_warehouse', 'driver', 'velos', 'velo_state', 'spare_parts', 'distance', 'get_googlemaps_link']
    search_fields = ['from_warehouse__name', 'to_warehouse__name', 'driver__name']
    list_filter = ['date', 'driver', 'velo_state', 'spare_parts']
    readonly_fields = ['get_googlemaps_link']
    changelist_actions = ['get_distances']
    change_actions = ['get_distance']
    actions = ['get_distances']

    def get_queryset(self, request):
        qs = super(RideAdmin, self).get_queryset(request)
        # superusers should see all entries
        if request.user.is_superuser:
            return qs
        # other users with a correlating person should only see their organisations entries
        elif hasattr(request.user, 'person'):
            return qs.filter(driver__organisation=request.user.person.organisation)
        # users with no superuser role and no related person should not see any entries
        else:
            return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'car':
            if request.user.is_superuser:
                pass
            # other users with a correlating person should only see their organisation
            elif hasattr(request.user, 'person'):
                kwargs["queryset"] = Car.objects.filter(organisation=request.user.person.organisation.id)
            # users with no superuser role and no related person should not see any organisations
            else:
                kwargs["queryset"] = Car.objects.none()
        return super(RideAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_distance(self, request, obj):
        result = obj.get_distance()
        print result
        if type(result) == int: 
            self.message_user(request, "Die Distanz zwischen {} und {} beträgt {} Meter.".format(obj.from_warehouse, obj.to_warehouse, result))
        else:
            self.message_user(request, "Die Distanz konnte nicht ermittelt werden.", level=messages.WARNING)
    get_distance.short_description = "Distanz berechnen"
    get_distance.label = "Distanz berechnen"

    def get_distances(self, request, queryset):
        count = 0
        for r in queryset:
            result = r.get_distance()
            if result:
                count += 1
        self.message_user(request, "Die Distanz wurde auf {} Adressen gesetzt.".format(count))
    get_distances.short_description = "Distanz berechnen"

    def get_googlemaps_link(self, obj):
        url = obj.get_googlemaps_url()
        if url:
            return mark_safe(u"<a href='{}' target='_blank'>{}</a>".format(
                url,
                "Auf Google Maps zeigen"
            ))
        else:
            return ""
    get_googlemaps_link.short_description = 'Google Maps'


admin.site.register(Car, CarAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(VeloState, VeloStateAdmin)
admin.site.register(Ride, RideAdmin)
