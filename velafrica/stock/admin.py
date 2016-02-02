# -*- coding: utf-8 -*-
from django.contrib import admin
from velafrica.stock.models import Product, Category, Warehouse, Stock, StockTransfer, StockTransferPosition
from import_export import resources
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin

class CategoryResource(resources.ModelResource):
    """
    Define the category resource for import / export.
    """

    class Meta:
        model = Category
        import_id_fields = ('name',)


class CategoryAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = CategoryResource
    list_display = ('name', 'description')
    search_fields = ['name', 'description']


class ProductResource(resources.ModelResource):
    """
    Define the Product resource for import / export.
    """

    class Meta:
        model = Product
        import_id_fields = ('articlenr',)
        fields = ('category', 'category__name', 'articlenr', 'hscode', 'name', 'price', 'description')


class ProductAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = ProductResource
    list_display = ('articlenr', 'hscode', 'category', 'name', 'price', 'description')
    search_fields = ['articlenr', 'name', 'description']
    list_filter = ['category']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Warehouse)
admin.site.register(Stock)
admin.site.register(StockTransfer)
admin.site.register(StockTransferPosition)