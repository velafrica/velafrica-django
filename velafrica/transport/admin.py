# -*- coding: utf-8 -*-
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from velafrica.stock.models import Warehouse
from velafrica.transport.models import Car, Driver, VeloState, Ride
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.fields import Field
from import_export.widgets import DateWidget, ForeignKeyWidget

class CarAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'organisation', 'plate']
    search_fields = ['name']


class DriverAdmin(SimpleHistoryAdmin):
    list_display = ['name']
    search_fields = ['name']


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


class RideAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = RideResource
    list_display = ['id', 'date', 'from_warehouse', 'to_warehouse', 'driver', 'velos', 'velo_state', 'spare_parts']
    search_fields = ['from_warehouse__name', 'to_warehouse__name', 'driver__name']
    list_filter = ['date', 'driver', 'velo_state', 'spare_parts']


admin.site.register(Car, CarAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(VeloState, VeloStateAdmin)
admin.site.register(Ride, RideAdmin)
