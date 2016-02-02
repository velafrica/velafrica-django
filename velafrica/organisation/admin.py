# -*- coding: utf-8 -*-
from django.contrib import admin
from velafrica.organisation.models import Organisation, Person
from velafrica.stock.models import Warehouse
from import_export import resources
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin

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

admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Person)
