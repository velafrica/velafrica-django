# -*- coding: utf-8 -*-
from decimal import Decimal

from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from velafrica.organisation.models import Organisation
from velafrica.stock.models import StockListPos


class InvoiceListPos(StockListPos):
    """
    """
    invoice = models.ForeignKey('Invoice')

    class Meta:
        unique_together = (("invoice", "product"),)


class Payment(models.Model):
    """
    """
    received_on = models.DateField(default=timezone.now, verbose_name="Eingangsdatum")
    amount = models.IntegerField()
    invoice = models.ForeignKey('Invoice')

    def __unicode__(self):
        return u"{} {} {}".format(self.received_on, self.amount, self.invoice)

class Invoice(models.Model):
    """
    """
    from_org = models.ForeignKey(Organisation, related_name='invoice_from', verbose_name="Rechnungssteller")
    to_org = models.ForeignKey(Organisation, related_name='invoice_to', verbose_name="Rechnungsempfänger")
    comments = models.TextField(blank=True, null=True, verbose_name="Kommentare")
    purchaseorder = models.ForeignKey('PurchaseOrder', blank=True, null=True, verbose_name="Kaufauftrag (Purchase Order)", help_text="Wird hier ein Kaufauftrag (Purchase Order) hinterlegt, wird für die Berechnung des Rechnungsbetrags der Einkaufspreis verwendet.")
    salesorder = models.ForeignKey('SalesOrder', blank=True, null=True, verbose_name="Kundenauftrag (Sales Order)")
    history = HistoricalRecords()

    def get_total(self):
        total = Decimal(0.00)
        print total
        pos = InvoiceListPos.objects.all().filter(invoice=self.id)

        if self.purchaseorder:
            for p in pos:
                total += p.product.get_purchase_price()
        else:
            for p in pos:
                print p.product.sales_price
                total += p.product.sales_price
        print total
        return total
    get_total.short_description = "Rechnungsbetrag"
    get_total.help_text = "Berechnet aus dem Verkaufspreis. Um Einkaufspreise zu verwenden, einen Purchase Order zur Rechnung verknüpfen"

    def get_total_payments(self):
        total = Decimal(0.00)
        pos = Payment.objects.all().filter(invoice=self.id)
        for p in pos:
            total += p.amount
        return total
    get_total_payments.short_description = "Eingegangene Zahlungen"


    def __unicode__(self):
        return u"Invoice #{}: {} an {} ".format(self.id, self.from_org, self.to_org)


class PurchaseOrderListPos(StockListPos):
    """
    One position of a :model:`commission.PurchaseOrder` including product and amount.
    """
    purchaseorder = models.ForeignKey('PurchaseOrder')

    def __unicode__(self):
        return u"PurchaseOrder #{}: {}x {} ".format(self.purchaseorder.id, self.amount, self.product)
        
    class Meta:
        unique_together = (("purchaseorder", "product"),)


class PurchaseOrder(models.Model):
    """
    PurchaseOrders represent orders from the issueing organisation to another (procurement).
    TODO:
      - create procurement (stock in)
    """
    from_org = models.ForeignKey(Organisation, related_name="purchaseorder_from", blank=True, null=True, verbose_name="Anbieter")
    to_org = models.ForeignKey(Organisation, related_name="purchaseorder_to", blank=True, null=True, verbose_name="Kunde")
    comments = models.TextField(blank=True, null=True, verbose_name="Kommentare")
    PO_STATE_CHOICES = {
        ('0', 'draft'),
        ('1', 'confirmed'),
        ('2', 'shipped'),
        ('3', 'invoiced'),
        ('4', 'complete')
    }
    state = models.CharField(choices=PO_STATE_CHOICES, verbose_name="Status", default='0', max_length=2)

    history = HistoricalRecords()

    def get_total(self):
        """
        Calculate total value of all :model:`commission.PurchaseOrderListPos` related to this PurchaseOrder.
        """
        total = Decimal(0.00)
        pos = PurchaseOrderListPos.objects.all().filter(purchaseorder=self.id)

        for p in pos:
            total += p.product.get_purchase_price()
        return total
    get_total.short_description = "Betrag"

    def copy_to_draft(self):
        """
        Copy current PurchaseOrder to a new one.
        """
        p = PurchaseOrder(from_org=self.from_org, to_org=self.to_org, state='0', comments="Kopie von {}".format(self))
        p.save()

        listpos = PurchaseOrderListPos.objects.filter(purchaseorder=self.id)

        for lp in listpos:
            polp = PurchaseOrderListPos(product=lp.product, amount=lp.amount, purchaseorder=p)
            polp.save()

        return p


    def create_invoice(self):
        """
        Create an invoice based on the PurchaseOrder.
        """
        sopos = PurchaseOrderListPos.objects.filter(purchaseorder=self.id)
        if sopos.count() > 0:
            inv = Invoice(from_org=self.from_org, to_org=self.to_org, purchaseorder=self, comments="Rechnung für {}".format(self))
            inv.save()
            for pos in sopos:
                ilp = InvoiceListPos(product=pos.product, amount=pos.amount, invoice=inv)
                ilp.save()
            return inv
        else:
            return False

    def __unicode__(self):
        return u"PurchaseOrder #{}: {} ".format(self.id, self.to_org)


class SalesOrderListPos(StockListPos):
    """

    """
    salesorder = models.ForeignKey('SalesOrder')

    def __unicode__(self):
        return u"PurchaseOrder #{}: {}x {} ".format(self.salesorder.id, self.amount, self.product)
        
    class Meta:
        unique_together = (("salesorder", "product"),)



class SalesOrder(models.Model):
    """
    SalesOrders represent offers from the issueing organisation to another (sales).
    TODO:
    - states
    - methods:
        - create picking list
        - create invoice
        - create picking (stock out)
        - create payment (partial?)
    """
    from_org = models.ForeignKey(Organisation, related_name="salesorder_from", blank=True, null=True, verbose_name="Anbieter")
    to_org = models.ForeignKey(Organisation, related_name="salesorder_to", blank=True, null=True, verbose_name="Kunde")
    comments = models.TextField(blank=True, null=True, verbose_name="Kommentare")
    history = HistoricalRecords()

    # container = models.ForeignKey(Container)

    def get_total(self):
        """
        Get total value of SalesOrder.
        """
        total = Decimal(0.00)
        pos = SalesOrderListPos.objects.all().filter(salesorder=self.id)

        for p in pos:
            total += p.product.sales_price
        return total
    get_total.short_description = "Betrag"

    def create_invoice(self):
        """
        Create invoice based on SalesOrder.
        """
        sopos = SalesOrderListPos.objects.filter(salesorder=self.id)
        if sopos.count() > 0:
            inv = Invoice(from_org=self.from_org, to_org=self.to_org, salesorder=self)
            inv.save()
            for pos in sopos:
                ilp = InvoiceListPos(product=pos.product, amount=pos.amount, invoice=inv)
                ilp.save()
            return sopos
        else:
            return False

    def __unicode__(self):
        return u"SalesOrder #{}: {} ".format(self.id, self.to_org)
