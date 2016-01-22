from django.contrib import admin
from stock.models import Product, Category
from simple_history.admin import SimpleHistoryAdmin

class CategoryAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'description')
    search_fields = ['name', 'description']

class ProductAdmin(SimpleHistoryAdmin):
    list_display = ('sku', 'name', 'description', 'category')
    search_fields = ['sku', 'name', 'description']
    list_filter = ['category']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)