from django.contrib import admin
from velafrica.stock.models import Product, Category
from import_export import resources
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin

class CategoryResource(resources.ModelResource):
    """
    Define the category resource for import / export.
    """

    class Meta:
        model = Category

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

class ProductAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = ProductResource
    list_display = ('sku', 'name', 'description', 'category')
    search_fields = ['sku', 'name', 'description']
    list_filter = ['category']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)