from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export import fields
from import_export import resources
from import_export.admin import ImportExportMixin, ExportMixin
from simple_history.admin import SimpleHistoryAdmin
from .models import TrackingStation, TrackingStationQuery


class TrackingStationQueryInlineAdmin(admin.TabularInline):
    model = TrackingStationQuery
    extra = 0
    min_num = 0


admin.site.register(TrackingStationQuery)
admin.site.register(TrackingStation)
