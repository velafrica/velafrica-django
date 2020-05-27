# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_object_actions import DjangoObjectActions
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin

from velafrica.stock.resources import ProductResource, WarehouseResource, StockResource, StockChangeResource, \
    StockListPositionResource, StockListResource, StockTransferResource, CategoryResource
from velafrica.stock.forms import StockForm, StockListPositionForm, StockListPosForm, StockTransferForm
from velafrica.stock.models import *
from velafrica.transport.models import Ride
from velafrica.velafrica_sud.models import Container


class CategoryAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = CategoryResource
    list_display = ('articlenr_start', 'name', 'description')
    search_fields = ['name', 'description']


class ProductAdmin(ImportExportMixin, SimpleHistoryAdmin):
    """
    """
    resource_class = ProductResource
    readonly_fields = ['get_purchase_price']
    list_display = ('admin_image', 'articlenr', 'name', 'hscode', 'category', 'get_purchase_price', 'sales_price',
                    'description')
    list_display_links = ('admin_image', 'articlenr', 'name',)
    search_fields = ['articlenr', 'name', 'description']
    list_filter = ['category']


class StockInline(admin.TabularInline):
    model = Stock


class StockAdmin(ImportExportMixin, SimpleHistoryAdmin):
    form = StockForm
    resource_class = StockResource
    list_display = ['__str__', 'product', 'warehouse', 'amount', 'last_modified']
    list_editable = ['amount']
    search_fields = ['product__name']
    list_filter = ['warehouse']
    readonly_fields = ['last_modified']

    def get_queryset(self, request):
        qs = super(StockAdmin, self).get_queryset(request)
        # superusers should see all entries
        if request.user.is_superuser or request.user.has_perm('stock.is_admin'):
            return qs
        # other users with a correlating person should only see their organisations entries
        elif hasattr(request.user, 'person'):
            return qs.filter(warehouse__organisation=request.user.person.organisation)
        # users with no superuser role and no related person should not see any entries
        else:
            return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'warehouse':
            if request.user.is_superuser or request.user.has_perm('stock.is_admin'):
                pass
            # other users with a correlating person should only see their organisation
            elif hasattr(request.user, 'person'):
                print("stock is not admin")
                kwargs["queryset"] = Warehouse.objects.filter(organisation=request.user.person.organisation.id)
            # users with no superuser role and no related person should not see any organisations
            else:
                kwargs["queryset"] = Warehouse.objects.none()
        return super(StockAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class StockChangeAdmin(ImportExportMixin, SimpleHistoryAdmin):
    resource_class = StockChangeResource
    model = StockChange
    list_display = ['datetime', 'stocktransfer', 'warehouse', 'stocklist', 'stock_change_type', 'booked']
    list_filter = ['warehouse', 'stock_change_type']
    search_fields = ['warehouse__name']


class WarehouseAdmin(ImportExportMixin, SimpleHistoryAdmin):
    inlines = [StockInline, ]
    resource_class = WarehouseResource
    list_display = ['name', 'organisation', 'description', 'stock_management', 'get_googlemaps_link']
    search_fields = ['name', 'description', 'organisation__name']
    list_filter = ['organisation', 'stock_management']
    readonly_fields = ['get_googlemaps_link']

    def get_googlemaps_link(self, obj):
        a = obj.get_address()
        if a:
            url = a.get_googlemaps_url()
            if url:
                return mark_safe(u"<a href='{}' target='_blank'>{}</a>".format(
                    url,
                    a
                ))
            else:
                return ""

    get_googlemaps_link.short_description = 'Google Maps'


class StockChangeInline(admin.TabularInline):
    model = StockChange
    readonly_fields = ['datetime', 'stocktransfer', 'warehouse', 'stocklist', 'stock_change_type', 'booked']

    # do not allow users to create new stock changes themselves
    def has_add_permission(self, request):
        return False


class StockListPositionAdmin(ImportExportMixin, SimpleHistoryAdmin):
    form = StockListPositionForm
    model = StockListPosition
    resource_class = StockListPositionResource
    list_display = ['id', 'product', 'amount', 'stocklist']
    list_filter = ['stocklist']
    search_fields = ['product__name', 'product__articlenr', 'stocklist__description']


class StockListPositionInline(admin.TabularInline):
    form = StockListPositionForm
    model = StockListPosition


class StockListInline(admin.TabularInline):
    inlines = [StockListPositionInline]
    model = StockList


class RideInline(admin.TabularInline):
    model = Ride


class StockTransferListPosInline(admin.TabularInline):
    model = StockTransferListPos
    form = StockListPosForm


class StockTransferInline(admin.TabularInline):
    model = StockTransfer


class ContainerInline(admin.TabularInline):
    model = Container


class StockListAdmin(ImportExportMixin, DjangoObjectActions, SimpleHistoryAdmin):
    """
    TODO: remove, StockList is deprecated
    """
    inlines = [StockListPositionInline]
    resource_class = StockListResource
    list_display = ['id', 'ride_link', 'stocktransfer_link', 'container_link', 'description', 'last_change',
                    'listpositions_link']
    search_fields = ['description']
    readonly_fields = ['ride_link', 'stocktransfer_link', 'container_link']

    def listpositions_link(self, obj):
        if obj.stocklistposition_set.first():
            r = 'admin:{}_{}_changelist'.format(obj.stocklistposition_set.first()._meta.app_label,
                                                obj.stocklistposition_set.first()._meta.model_name)
            print(r)
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


class StockTransferAdmin(ImportExportMixin, DjangoObjectActions, SimpleHistoryAdmin):
    # inlines = [StockChangeInline, StockTransferListPosInline]
    inlines = [StockChangeInline]
    form = StockTransferForm
    resource_class = StockTransferResource
    list_display = ['id', 'date', 'warehouse_from', 'warehouse_to', 'stocklist', 'booked', 'note']
    list_filter = ['date', 'warehouse_from', 'warehouse_to', 'booked']
    readonly_fields = ['booked']
    actions = ['book_stocktransfers', 'fake_book_stocktransfers', 'revoke_stocktransfer']
    changelist_actions = ['book_stocktransfers', 'fake_book_stocktransfers', 'revoke_stocktransfers']
    change_actions = ['book_stocktransfer', 'fake_book_stocktransfer', 'revoke_stocktransfer']

    def fake_book_stocktransfer(self, request, obj):
        """
        Admin action to book a single StockTransfer without changing any stocks.
        """
        if obj:
            if obj.book(fake=True):
                self.message_user(request, "StockTransfer %s erfolgreich fake verbucht." % obj.id)
            else:
                self.message_user(request, "StockTransfer %s wurde bereits verbucht." % obj.id)
        else:
            self.message_user(request, "Not sure which StockTransfer to book." % obj.id)

    fake_book_stocktransfer.short_description = "StockTransfer Fake Verbuchen"
    fake_book_stocktransfer.label = "Fake Verbuchen"

    def book_stocktransfer(self, request, obj):
        """
        Admin action to book a single StockTransfer.
        """
        if obj:
            if obj.book():
                self.message_user(request, "StockTransfer %s erfolgreich verbucht." % obj.id)
            else:
                self.message_user(request, "StockTransfer %s wurde bereits verbucht." % obj.id)
        else:
            self.message_user(request, "Not sure which StockTransfer to book." % obj.id)

    book_stocktransfer.short_description = "StockTransfer Verbuchen"
    book_stocktransfer.label = "Verbuchen"

    def book_stocktransfers(self, request, queryset, fake=False):
        """
        Admin action to book StockTransfers.
        TODO: signals
        """
        rows_updated = 0
        for obj in queryset:
            if obj.book(fake=fake):
                rows_updated += 1

        if rows_updated == 1:
            message_bit = "1 StockTransfer "
        else:
            message_bit = "%s StockTransfer " % rows_updated
        self.message_user(request, "%s erfolgreich verbucht." % message_bit)

    book_stocktransfers.short_description = "Ausgewählte StrockTransfers verbuchen"
    book_stocktransfers.label = "Verbuchen"

    def fake_book_stocktransfers(self, request, queryset):
        self.book_stocktransfers(request, queryset, fake=True)

    fake_book_stocktransfers.short_description = "Ausgewählte StrockTransfers Fake verbuchen"
    fake_book_stocktransfers.label = "Fake Verbuchen"

    def revoke_stocktransfer(self, request, obj):
        """
        Admin action to book a single StockTransfer.
        """
        if obj:
            if obj.revoke():
                self.message_user(request, "StockTransfer %s erfolgreich zurück gebucht." % obj.id)
            else:
                self.message_user(request, "StockTransfer %s ist momentan noch nicht verbucht." % obj.id)
        else:
            self.message_user(request, "Not sure which StockTransfer to revoke." % obj.id)

    revoke_stocktransfer.short_description = "StockTransfer zurückbuchen"
    revoke_stocktransfer.label = "Zurückbuchen"

    def revoke_stocktransfers(self, request, queryset):
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

    revoke_stocktransfer.short_description = "StockTransfer zurückbuchen"
    revoke_stocktransfer.label = "Zurückbuchen"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(StockChange, StockChangeAdmin)
admin.site.register(StockTransfer, StockTransferAdmin)
admin.site.register(StockList, StockListAdmin)
admin.site.register(StockListPosition, StockListPositionAdmin)

"""
admin.site.register(StockPosition)
admin.site.register(StockTaking)
admin.site.register(StockTakingStockPosition)
admin.site.register(StockIn)
admin.site.register(StockInStockPosition)
"""
