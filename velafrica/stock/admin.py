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
        import_id_fields = ('articlenr_start',)
        fields = ('articlenr_start', 'name', 'description')


class CategoryAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = CategoryResource
    list_display = ('articlenr_start', 'name', 'description')
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
    """
    """
    resource_class = ProductResource
    list_display = ('articlenr', 'hscode', 'category', 'name', 'price', 'description')
    search_fields = ['articlenr', 'name', 'description']
    list_filter = ['category']


class WarehouseResource(resources.ModelResource):
    """
    """
    class Meta:
        model = Warehouse

class StockInline(admin.TabularInline):
    model = Stock


class StockAdmin(SimpleHistoryAdmin):
    list_display = ['__unicode__', 'product', 'warehouse', 'amount', 'last_modified']
    list_editable = ['amount']
    search_fields = ['product']
    list_filter = ['warehouse']
    readonly_fields = ['last_modified']


class WarehouseAdmin(ImportExportMixin, SimpleHistoryAdmin):
    inlines = [StockInline,]
    resource_class = WarehouseResource
    list_display = ['name', 'organisation', 'description', 'stock_management']
    search_fields = ['name', 'description', 'organisation']
    list_filter = ['organisation', 'stock_management']


class StockTransferPositionInline(admin.TabularInline):
    model = StockTransferPosition


class StockTransferAdmin(SimpleHistoryAdmin):
    inlines = [StockTransferPositionInline,]
    list_display = ['id', 'date', 'warehouse_from', 'warehouse_to', 'executor', 'booked']
    list_filter = ['date', 'warehouse_from', 'warehouse_to', 'executor', 'booked']
    readonly_fields = ['booked']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(StockTransfer, StockTransferAdmin)
admin.site.register(StockTransferPosition)