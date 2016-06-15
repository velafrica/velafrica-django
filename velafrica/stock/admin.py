# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from velafrica.stock.models import *
from velafrica.stock.forms import StockForm, StockListPositionForm
from velafrica.transport.models import Ride
from velafrica.velafrica_sud.models import Container
from import_export import resources
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin
from import_export.fields import Field
from import_export.widgets import DateWidget, ForeignKeyWidget, ManyToManyWidget

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
        fields = ('category', 'category__name', 'articlenr', 'hscode', 'name', 'name_en', 'name_fr', 'packaging_unit', 'price', 'description')


class ProductAdmin(ImportExportMixin, SimpleHistoryAdmin):
    """
    """
    resource_class = ProductResource
    list_display = ('admin_image', 'articlenr', 'hscode', 'category', 'name', 'price', 'description')
    search_fields = ['articlenr', 'name', 'description']
    list_filter = ['category']


class WarehouseResource(resources.ModelResource):
    """
    """
    class Meta:
        model = Warehouse

class StockInline(admin.TabularInline):
    model = Stock


class StockResource(resources.ModelResource):
    """
    Define the Stock resource for import / export.
    """

    class Meta:
        model = Stock
        fields = ('product__articlenr', 'product', 'product__name', 'warehouse', 'warehouse__name', 'amount', 'last_modified')


class StockAdmin(ImportExportMixin, SimpleHistoryAdmin):
    form = StockForm
    resource_class = StockResource
    list_display = ['__unicode__', 'product', 'warehouse', 'amount', 'last_modified']
    list_editable = ['amount']
    search_fields = ['product__name']
    list_filter = ['warehouse']
    readonly_fields = ['last_modified']

    def get_queryset(self, request):
        qs = super(StockAdmin, self).get_queryset(request)
        # superusers should see all entries
        if request.user.is_superuser:
            return qs
        # other users with a correlating person should only see their organisations entries
        elif hasattr(request.user, 'person'):
            return qs.filter(warehouse__organisation=request.user.person.organisation)
        # users with no superuser role and no related person should not see any entries
        else:
            return []

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'warehouse':
            if request.user.is_superuser:
                pass
            # other users with a correlating person should only see their organisation
            elif hasattr(request.user, 'person'):
                kwargs["queryset"] = Warehouse.objects.filter(organisation=request.user.person.organisation.id)
            # users with no superuser role and no related person should not see any organisations
            else:
                kwargs["queryset"] = []
        return super(StockAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class StockChangeResource(resources.ModelResource):
    """
    Define the StockChange resource for import / export.
    """

    class Meta:
        model = StockChange


class StockChangeAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = StockChangeResource
    model = StockChange
    list_display = ['datetime', 'stocktransfer', 'warehouse', 'stocklist', 'stock_change_type']
    list_filter = ['warehouse', 'stock_change_type']
    search_fields = ['warehouse__name']


class WarehouseAdmin(ImportExportMixin, SimpleHistoryAdmin):
    inlines = [StockInline,]
    resource_class = WarehouseResource
    list_display = ['name', 'organisation', 'description', 'stock_management']
    search_fields = ['name', 'description', 'organisation__name']
    list_filter = ['organisation', 'stock_management']


class StockChangeInline(admin.TabularInline):
    model = StockChange
    readonly_fields = ['datetime', 'stocktransfer', 'warehouse', 'stocklist', 'stock_change_type']

    # do not allow users to create new stock changes themselves
    def has_add_permission(self, request):
        return False


class StockListPositionResource(resources.ModelResource):
    """
    """
    class Meta:
        model = StockListPosition


class StockListPositionAdmin(ImportExportMixin, SimpleHistoryAdmin):
    form = StockListPositionForm
    model = StockListPosition
    resource_class = StockListPositionResource
    list_display = ['id', 'product', 'amount', 'stocklist']
    list_filter = ['stocklist']
    search_fields = ['product__name', 'product__articlenr', 'stocklist__description']


class StockListResource(resources.ModelResource):
    """

    """
    class Meta:
        model = StockList


class StockListPositionInline(admin.TabularInline):
    form = StockListPositionForm
    model = StockListPosition


class StockListInline(admin.TabularInline):
    inlines = [StockListPositionInline]
    model = StockList

class RideInline(admin.TabularInline):
    model = Ride

class StockTransferInline(admin.TabularInline):
    model = StockTransfer

class ContainerInline(admin.TabularInline):
    model = Container

class StockListAdmin(ImportExportMixin, SimpleHistoryAdmin):
    inlines = [StockListPositionInline]
    resource_class = StockListResource
    list_display = ['id', 'ride_link', 'stocktransfer_link', 'container_link', 'description', 'last_change', 'listpositions_link']
    search_fields = ['description']
    readonly_fields = ['ride_link', 'stocktransfer_link', 'container_link']


    def listpositions_link(self, obj):
        if obj.stocklistposition_set.first():
            r = 'admin:{}_{}_changelist'.format(obj.stocklistposition_set.first()._meta.app_label, obj.stocklistposition_set.first()._meta.model_name)
            print r
            return mark_safe('<a href="{}?stocklist__id__exact={}">{}</a>'.format(
                reverse(r, args=[]),
                obj.id,
                obj.size()
            ))
        return None
    listpositions_link.short_description = 'Anzahl Positionen'

    def ride_link(self, obj):
        r = 'admin:{}_{}_change'.format(obj.ride._meta.app_label, obj.ride._meta.model_name)
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse(r, args=(obj.ride.id,)),
            obj.ride
        ))
    ride_link.short_description = 'Ride'

    def stocktransfer_link(self, obj):
        r = 'admin:{}_{}_change'.format(obj.stocktransfer._meta.app_label, obj.stocktransfer._meta.model_name)
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse(r, args=(obj.stocktransfer.id,)),
            obj.stocktransfer
        ))
    stocktransfer_link.short_description = 'StockTransfer'

    def container_link(self, obj):
        r = 'admin:{}_{}_change'.format(obj.container._meta.app_label, obj.container._meta.model_name)
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse(r, args=(obj.container.id,)),
            obj.container
        ))
    container_link.short_description = 'Container'


class StockTransferResource(resources.ModelResource):
    """

    """
    class Meta:
        model = StockTransfer


class StockTransferAdmin(ImportExportMixin, SimpleHistoryAdmin):
    inlines = [StockChangeInline]
    resource_class = StockTransferResource
    list_display = ['id', 'date', 'warehouse_from', 'warehouse_to', 'stocklist', 'booked', 'note']
    list_filter = ['date', 'warehouse_from', 'warehouse_to', 'booked']
    readonly_fields = ['booked']
    actions = ['book_stocktransfer', 'revoke_stocktransfer']

    def book_stocktransfer(self, request, queryset):
        """
        Admin action to book StockTransfers.
        TODO: signals
        """
        rows_updated = 0
        for obj in queryset:
            if obj.book():
                rows_updated += 1

        if rows_updated == 1:
            message_bit = "1 StockTransfer was"
        else:
            message_bit = "%s StockTransfer were" % rows_updated
        self.message_user(request, "%s booked successfully." % message_bit)
    book_stocktransfer.short_description = "Book selected StrockTransfers"


    def revoke_stocktransfer(self, request, queryset):
        """
        Admin action to revoke StockTransfers.
        TODO: signals
        """
        rows_updated = 0
        for obj in queryset:
            if obj.revoke():
                rows_updated += 1
        if rows_updated == 1:
            message_bit = "1 StockTransfer was"
        else:
            message_bit = "%s StockTransfer were" % rows_updated
        self.message_user(request, "%s revoked successfully." % message_bit)
    revoke_stocktransfer.short_description = "Revoke selected StrockTransfers"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(StockChange, StockChangeAdmin)
admin.site.register(StockTransfer, StockTransferAdmin)
admin.site.register(StockList, StockListAdmin)
admin.site.register(StockListPosition, StockListPositionAdmin)
