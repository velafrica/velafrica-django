from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from velafrica.collection.models import *
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.fields import Field
from import_export.widgets import DateWidget
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(CollectionEvent)
admin.site.register(CollectionEventType)
admin.site.register(CollectionPartner)
admin.site.register(CollectionEventTask)
admin.site.register(CollectionEventTaskStatus)
admin.site.register(CollectionEventTaskProgress)