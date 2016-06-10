# -*- coding: utf-8 -*-
from django.contrib import admin
from velafrica.organisation.models import Organisation, Person, Canton, Municipality
from velafrica.stock.models import Warehouse
from import_export import resources
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

"""
class WarehouseInline(admin.StackedInline):
	model = Warehouse
"""

class OrganisationResource(resources.ModelResource):
    """
    Define the organisation resource for import / export.
    """

    class Meta:
        model = Organisation


class OrganisationAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = OrganisationResource
    # inlines = [WarehouseInline,]
    list_display = ('name', 'street', 'plz', 'city', 'website')
    search_fields = ['name', 'city']


class CantonResource(resources.ModelResource):
    """
    Define the organisation resource for import / export.
    """

    class Meta:
        model = Canton
        import_id_fields = ('short',)

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

    class Meta:
        model = Canton
        canton = Field(
            column_name='canton',
            attribute='canton',
            widget=ForeignKeyWidget(Warehouse, 'short'))
        import_id_fields = ('gdenr',)


class MunicipalityAdmin(ImportExportMixin, SimpleHistoryAdmin):
    """
    """
    resource_class = MunicipalityResource
    list_display = ['plz', 'plz_name', 'canton']
    search_fields = ['plz', 'plz_name', 'canton__name']
    list_filter = ['canton__name']


admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Person)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Canton, CantonAdmin)

