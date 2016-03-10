from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from velafrica.counter.models import Entry
from velafrica.organisation.models import Organisation
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.fields import Field
from import_export.widgets import DateWidget
from simple_history.admin import SimpleHistoryAdmin

class EntryResource(resources.ModelResource):
    """
    Define the resource for counter entry.
    """
    date = Field(
        column_name='date',
        attribute='date',
        widget=DateWidget(format="%d.%m.%Y"))

    class Meta:
        model = Entry

class EntryAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = EntryResource
    list_display = ('date', 'organisation', 'amount', 'note')
    search_fields = ['note', 'organisation']
    list_editable = ['amount', 'note']
    list_filter = (
        'date', 
        ('date', DateRangeFilter),
        'organisation'
        )

    def get_queryset(self, request):
        qs = super(EntryAdmin, self).get_queryset(request)
        # superusers should see all entries
        if request.user.is_superuser:
            return qs
        # other users with a correlating person should only see their organisations entries
        elif hasattr(request.user, 'person'):
            return qs.filter(organisation=request.user.person.organisation)
        # users with no superuser role and no related person should not see any entries
        else:
            return []

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'organisation':
            if request.user.is_superuser:
                pass
            # other users with a correlating person should only see their organisation
            elif hasattr(request.user, 'person'):
                kwargs["queryset"] = Organisation.objects.filter(id=request.user.person.organisation.id)
            # users with no superuser role and no related person should not see any organisations
            else:
                kwargs["queryset"] = []
        return super(EntryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Entry, EntryAdmin)