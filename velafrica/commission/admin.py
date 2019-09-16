# -*- coding: utf-8 -*-
from django import template
from django_object_actions import DjangoObjectActions
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.shortcuts import redirect
from velafrica.commission.models import *
from velafrica.stock.forms import StockListPosForm
from velafrica.stock.models import StockTransfer
from velafrica.velafrica_sud.models import Container
from import_export import resources
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin
from import_export.fields import Field


class SalesOrderListPosInline(admin.TabularInline):
    model = SalesOrderListPos
    form = StockListPosForm

class PurchaseOrderListPosInline(admin.TabularInline):
    model = PurchaseOrderListPos
    form = StockListPosForm

    extra = 0
    editable_fields = []
    fields = ['product', 'amount']

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.state != '0':
            fields = []
            for field in self.model._meta.get_fields():
                if (not field == 'id'):
                    #if (field not in self.editable_fields):
                        fields.append(field)
            return fields
        else:
            return []

    def has_delete_permission(self, request, obj=None):
        if obj and obj.state != '0':
            return False
        else:
            return True

class InvoiceListPosInline(admin.TabularInline):
    model = InvoiceListPos
    form = StockListPosForm
    readonly_fields = ['get_purchase_price', 'get_sales_price']


class PurchaseOrderAdmin(DjangoObjectActions, SimpleHistoryAdmin):
    """
    """
    model = PurchaseOrder
    inlines = [PurchaseOrderListPosInline]
    fields = ['from_org', 'to_org', 'state', 'comments']
    list_display = ['__str__', 'from_org', 'to_org', 'state', 'comments', 'get_total']
    readonly_fields = ['id', 'state', 'get_total']
    change_actions = ['confirm', 'ship', 'create_invoice', 'mark_complete', 'copy_to_draft']


    
    def get_readonly_fields(self, request, obj=None):
        print(obj)
        if obj and obj.state != '0':
            fields = []
            for field in self.model._meta.get_fields():
                if (not field == 'id'):
                    #if (field not in self.editable_fields):
                        fields.append(field)
            fields.remove('purchaseorderlistpos')
            fields.remove('invoice')
            return fields
        else:
            return ['state']    

    def get_change_actions(self, request, object_id, form_url):
        all_actions = super(PurchaseOrderAdmin, self).get_change_actions(request, object_id, form_url)
        all_actions = list(all_actions)
        actions = []

        obj = self.model.objects.get(pk=object_id)
        if obj.state == '0':
            actions.append('confirm')
            #actions = actions.remove('confirm')
        elif obj.state == '1':
            actions.append('ship')
        elif obj.state == '2':
            actions.append('create_invoice')
        elif obj.state == '3':
            actions.append('mark_complete')

        actions.append('copy_to_draft')
        
        return actions

    def copy_to_draft(self, request, obj):
        result = obj.copy_to_draft()
        r = 'admin:{}_{}_change'.format(result._meta.app_label, result._meta.model_name)
        self.message_user(request, u"Neuen PurchaseOrder {} als Kopie von PurchaseOrder {} angelegt. Änderungen können direkt hier vorgenommen und gespeichert werden.".format(result.id, obj.id))
        return redirect(reverse(r, args=(result.id,)))
    copy_to_draft.short_description = "Neuen PurchaseOrder als Kopie"
    copy_to_draft.label = "Neuen PurchaseOrder als Kopie"


    def confirm(self, request, obj):
        obj.state = '1'
        obj.save()
        self.message_user(request, u"PurchaseOrder {} bestätigt.".format(obj.id))
    confirm.short_description = "Bestätigen"
    confirm.label = "Bestätigen"
        
    def ship(self, request, obj):
        obj.state = '2'
        obj.save()
        self.message_user(request, u"PurchaseOrder {} als versandt markiert.".format(obj.id))
    ship.short_description = "Versand"
    ship.label = "Versand"

    def create_invoice(self, request, obj):
        """
        Admin action to book a container.
        """
        if obj:
            result = obj.create_invoice()
            if result:
                self.message_user(request, u"Rechnung {} erfolgreich erstellt.".format(result))
                obj.state = '3'
                obj.save()
                r = 'admin:{}_{}_change'.format(result._meta.app_label, result._meta.model_name)
                return redirect(reverse(r, args=(result.id,)))
            else:
                self.message_user(request, u"Rechnung {} konnte nicht erstellt werden.".format(obj.id))
        else:
            self.message_user(request, "Not sure which PurchaseOrder to create invoice for." % obj.id)
    create_invoice.short_description = "Rechnung erstellen"
    create_invoice.label = "Rechnung erstellen"

    def mark_complete(self, request, obj):
        obj.state = '4'
        obj.save()
        self.message_user(request, u"PurchaseOrder {} fertiggestellt.".format(obj.id))


class SalesOrderAdmin(SimpleHistoryAdmin):
    model = SalesOrder
    inlines = [SalesOrderListPosInline]
    change_actions = ['create_invoice']
    list_display = ['__str__', 'from_org', 'to_org', 'comments', 'get_total']
    readonly_fields = ['get_total']

    def create_invoice(self, request, obj):
        """
        Admin action to book a container.
        """
        if obj:
            result = obj.create_invoice()
            if result:
                self.message_user(request, u"Rechnung {} erfolgreich erstellt.".format(result.id))
            else:
                self.message_user(request, u"Rechnung {} konnte nicht erstellt werden.".format(obj.id))
        else:
            self.message_user(request, "Not sure which SalesOrder to create invoice for." % obj.id)
        
    create_invoice.short_description = "Rechnung erstellen"
    create_invoice.label = "Rechnung erstellen"


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

class InvoiceAdmin(SimpleHistoryAdmin):
    model = Invoice
    inlines = [InvoiceListPosInline, PaymentInline]
    readonly_fields = ['get_total', 'get_total_payments']
    list_display = ['__str__', 'from_org', 'to_org', 'comments', 'get_total', 'get_total_payments']

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(SalesOrder, SalesOrderAdmin)
