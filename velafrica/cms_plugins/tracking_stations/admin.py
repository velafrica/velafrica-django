from django.contrib import admin
from .models import TrackingStation, TrackingStationQuery
from .forms import TrackingStationQueryInlineAdminForm

class TrackingStationQueryInlineAdmin(admin.TabularInline):
    # form = TrackingStationQueryInlineAdminForm
    model = TrackingStationQuery
    extra = 0
    min_num = 0


admin.site.register(TrackingStationQuery)
admin.site.register(TrackingStation)
