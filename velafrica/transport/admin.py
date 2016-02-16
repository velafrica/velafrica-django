# -*- coding: utf-8 -*-
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from velafrica.transport.models import Car, Driver, VeloState, Ride


class CarAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'organisation', 'plate']
    search_fields = ['name']


class DriverAdmin(SimpleHistoryAdmin):
    list_display = ['name']
    search_fields = ['name']


class VeloStateAdmin(SimpleHistoryAdmin):
    list_display = ['name']
    search_fields = ['name']


class RideAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'date', 'from_warehouse', 'to_warehouse', 'driver', 'velos', 'velo_state', 'spare_parts']
    search_fields = ['from_warehouse', 'to_warehouse', 'driver']
    list_filter = ['date', 'driver', 'velo_state', 'spare_parts']

admin.site.register(Car, CarAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(VeloState, VeloStateAdmin)
admin.site.register(Ride, RideAdmin)
