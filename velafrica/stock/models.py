# -*- coding: utf-8 -*-
from django.utils import timezone
from django.core.validators import RegexValidator
from django.conf import settings
from django.db import models
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords
from velafrica.organisation.models import Person, Organisation, Municipality

from velafrica.core.ftp import MyFTPStorage
fs = MyFTPStorage()

class Category(models.Model):
    """
    Represents a product category.
    """
    articlenr_start = models.CharField(blank=True, null=True, max_length=8, verbose_name="Kategorienummer", unique=True, help_text="")
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Kategoriebezeichnung")
    description = models.TextField(blank=True, null=True, verbose_name="Beschreibung")
    image = ResizedImageField(storage=fs, size=[500, 500], upload_to='stock/categories/', blank=True, null=True, help_text='Product picture.')
    color = models.CharField(
        validators=[
            RegexValidator(
                regex="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", 
                message="Must be a hexcode (e.g. #000 or #000000)",
                code="invalid_hexcode"
            )
        ],
        help_text="Colour code to use for this category (hex value, i.e. #000 or #000000)",
        blank=True,
        null=True,
        max_length=7
    )
    history = HistoricalRecords()

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['articlenr_start', 'name']


class Product(models.Model):
    """
    Represents a product.
    """
    articlenr = models.CharField(blank=False, null=False, max_length=7, verbose_name="Artikelnummer", unique=True, help_text="Die Velafrica Artikelnummer (in der Form 123.123)")
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Produktbezeichnung")
    name_fr = models.CharField(blank=True, null=True, max_length=255, verbose_name="Produktbezeichnung FR")
    name_en = models.CharField(blank=True, null=True, max_length=255, verbose_name="Produktbezeichnung EN")
    hscode = models.CharField(blank=False, null=False, max_length=7, verbose_name="Harmonized System Code")
    description = models.TextField(blank=True, null=True, verbose_name="Beschreibung", help_text="Hinweise zur Qualität bzw Hinweise und Ergänzung")
    category = models.ForeignKey('Category', verbose_name="Kategorie", help_text='Die Hauptkategorie des Produktes.')
    image = ResizedImageField(storage=fs, size=[500, 500], upload_to='stock/products/', blank=True, null=True, verbose_name="Produktbild")
    price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    packaging_unit = models.IntegerField(blank=True, null=True, verbose_name="Verpackungseinheit (VE)")
    history = HistoricalRecords()

    def admin_image(self):
        return ('<img src="{}{}" style="max-height: 100px;" />'.format(settings.MEDIA_URL, self.image))
    admin_image.allow_tags = True

    def __unicode__(self):
        return u"{}: {}".format(self.articlenr, self.name)

    class Meta:
        ordering = ['articlenr']


class Warehouse(models.Model):
    """
    TODO: everything
    - Name
    - Organisation
    - Adresse
    - Beschreibung
    """
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Name", help_text="Der Name / Bezeichnung des Lagers")
    description = models.CharField(blank=True, null=True, max_length=255, verbose_name="Beschreibung", help_text="Beschreibung / Bemerkungen zum Lager")
    organisation = models.ForeignKey(Organisation, verbose_name="Organisation", help_text='Die Organisation zu welcher das Lager gehört.')
    image = ResizedImageField(storage=fs, size=[500, 500], upload_to='stock/warehouses/', blank=True, null=True, verbose_name="Bild des Lagers")
    

    # address
    municipality = models.ForeignKey(Municipality, null=True, blank=True, verbose_name="Ort")
    street = models.CharField(blank=True, null=True, verbose_name="Strasse", max_length=255)
    lng = models.DecimalField(blank=True,null=True,verbose_name="Longitude (Längengrad)", max_digits=9, decimal_places=6)
    lat = models.DecimalField(blank=True,null=True,verbose_name="Latitude (Breitengrad)", max_digits=9, decimal_places=6)

    stock_management = models.BooleanField(default=False, verbose_name="Automatisches Stock-Management", help_text="Gibt an ob automatisches Stock-Management aktiviert ist, d.h. ob bei Stock Verschiebungen der Stock automatisch angepasst werden soll.")
    notify_on_incoming_transport = models.TextField(null=True, blank=True, verbose_name="Über angeliferte Ersatzteile informieren", help_text="Eine Emailadressen pro Zeile. Hier eingetragene Emailadressen werden jedesmal benachrichtigt, sobald eine neue Fahrt  mit Ersatzteilen zu diesem Lager erfasst wird.")
    history = HistoricalRecords()

    
    def __unicode__(self):
        return u"{}, {}".format(self.organisation.name, self.name)

    class Meta:
        ordering = ['organisation', 'name']


class Stock(models.Model):
    """
    TODO: everything
    - Warehouse
    - Product
    - amount
    """
    product = models.ForeignKey(Product, verbose_name="Produkt")
    warehouse = models.ForeignKey(Warehouse, verbose_name="Lager", help_text='Das Lager wo sich der Stock befindet')
    amount = models.IntegerField(blank=False, null=False, default=0, verbose_name="Stückzahl", help_text="Anzahl der Produkte an Lager")
    last_modified = models.DateTimeField(auto_now=True, help_text="Tag und Zeit wann das Objekt zuletzt geändert wurde.")
    history = HistoricalRecords()

    def __unicode__(self):
        return u"{}: {} x {}".format(self.warehouse.name, self.amount, self.product.name)

    class Meta:
        ordering = ['warehouse', 'product']
        unique_together = (("product", "warehouse"),)
        permissions = (
            ("is_admin", "Stock Admin - Can edit all stocks from every warehouse."),
        )


class StockList(models.Model):
    """
    TODO: remove
    A StockList is an universal object that can be used in various contexts,
    like as a payload inventory of a container or a transport, or as an inventory
    of an internal stock transfer.
    """
    last_change = models.DateTimeField(default=timezone.now)
    description = models.CharField(blank=True, null=True, max_length=255)
    #stocktransfer = models.OneToOneField('StockTransfer', blank=True, null=True)

    history = HistoricalRecords()

    def __unicode__(self):
        return u"SL#{0} - {1} ({2:%d.%m.%Y}, {3}:{2:%M})".format(self.id, self.description, self.last_change, self.last_change.hour+2)

    def get_stocktransfer(self):
        if self.stocktransfer:
            return self.stocktransfer
        return None
    get_stocktransfer.short_description = 'Stock Transfer'

    def get_ride(self):
        if self.ride:
            return self.ride
        return None
    get_ride.short_description = 'Ride'

    def get_container(self):
        if self.container:
            return self.container
        return None
    get_container.short_description = 'Container'

    def size(self):
        elem = StockListPosition.objects.filter(stocklist=self)
        return elem.count()
    size.short_description = 'Anzahl Positionen'


class StockListPosition(models.Model):
    """
    TODO: remove
    One position in a StockList.
    """
    stocklist = models.ForeignKey('StockList', verbose_name='StockList')
    product = models.ForeignKey(Product)
    amount = models.IntegerField(blank=False, null=False, verbose_name="Stückzahl")
    history = HistoricalRecords()

    class Meta:
        unique_together = (("stocklist", "product"),)

    def __unicode__(self):
        return u"StockList #{}: {}x {} ".format(self.stocklist.id, self.amount, self.product)


class StockListPos(models.Model):
    """
    Abstract BaseClass for all stock list position models.
    """
    product = models.ForeignKey(Product)
    amount = models.IntegerField(blank=False, null=False, verbose_name="Stückzahl", default=0)
    history = HistoricalRecords()

    class Meta:
        abstract = True


class StockChange(models.Model):
    """
    StockChange objects are used to keep track of all the stock changes per warehouse.
    StockChange objects never get created by the user directly, but when booking a StockTransfer.
    On pre_save, the application checks on the warehouse if stock is managed automatically.
    If so, the stock for all the objects in the StockList will be adjusted depending on the stock change type.
    On pre_delete, the application undoes the stock changes and then deletes the StocChange object.
    
    TODO: change usage, implement book()
    """
    STOCK_CHANGE_TYPES = {
        ('in', 'in'),
        ('out', 'out')
    }
    datetime = models.DateTimeField(default=timezone.now)
    stocktransfer = models.ForeignKey('StockTransfer')
    warehouse = models.ForeignKey(Warehouse)
    stocklist = models.ForeignKey(StockList)
    stock_change_type = models.CharField(choices=STOCK_CHANGE_TYPES, max_length=255)
    booked = models.BooleanField(default=False)

    def __unicode__(self):
        return u"StockChange {}, {} {}".format(self.datetime, self.stock_change_type, self.warehouse)

class StockChangeListPos(StockListPos):
    stockchange = models.ForeignKey(StockChange)


class StockTransfer(models.Model):
    """
    A StockTransfer object represents the moving of a stock from one warehouse to another.
    It can bee 'booked', which creates a new StockChange object for the 'from' and the 'to' warehouse
    and sets self.booked to True. The StockChange will get a deep copy of the StockList.
    Revoking a StockTransfer will delete the StockChange objects and reset
    self.booked to False.    
    """
    date = models.DateField(blank=False, null=False, default=timezone.now, verbose_name="Ausführdatum")
    warehouse_from = models.ForeignKey(Warehouse, related_name="warehouse_from", verbose_name="Herkunfts-Lager")
    warehouse_to = models.ForeignKey(Warehouse, related_name="warehouse_to", verbose_name="Ziel-Lager")
    stocklist = models.OneToOneField(StockList, verbose_name="Stock List")
    note = models.CharField(blank=True, null=True, max_length=255, verbose_name="Bemerkungen")
    booked = models.BooleanField(default=False, null=False, blank=False, help_text="Gibt an ob der Stock bereits angepasst wurde.")
    history = HistoricalRecords()

    def book(self):
        """
        - check if warehouse enabled auto stock update
        - adjust stock
        - create StockChange
        - set booked to True
        TODO: email notifications
        """
        if self.booked:
            print("Already booked, no action.")
            return False

        if self.warehouse_from.stock_management:
            # for each position in the stock list, update the warehouse stock
            for pos in StockListPosition.objects.filter(stocklist=self.stocklist.id):
                stock, created = Stock.objects.get_or_create(
                    product=pos.product,
                    warehouse=self.warehouse_from
                )
                stock.amount -= pos.amount
                stock.save()
            # create StockChange
            sc = StockChange(
                stocktransfer=self, 
                warehouse=self.warehouse_from,
                stocklist=self.stocklist,
                stock_change_type='out'
            )
            sc.save()
        if self.warehouse_to.stock_management:
            # for each position in the stock list, update the warehouse stock
            for pos in StockListPosition.objects.filter(stocklist=self.stocklist.id):
                stock, created = Stock.objects.update_or_create(
                    product=pos.product,
                    warehouse=self.warehouse_to
                )
                stock.amount += pos.amount
                stock.save()
            # create StockChange
            sc = StockChange(
                stocktransfer=self,
                warehouse=self.warehouse_to, 
                stocklist=self.stocklist, 
                stock_change_type='in'
            )
            sc.save()
        self.booked = True
        self.save()
        return True

    def revoke(self):
        """
        - check if warehouse enabled auto stock update
        - adjust stock
        - create StockChange
        - set booked to True
        TODO: email notifications
        """
        if not self.booked:
            print("Not booked yet, no action.")
            return False

        if self.warehouse_from.stock_management:
            # for each position in the stock list, update the warehouse stock
            for pos in StockListPosition.objects.filter(stocklist=self.stocklist.id):
                stock, created = Stock.objects.get_or_create(
                    product=pos.product,
                    warehouse=self.warehouse_from
                )
                stock.amount += pos.amount
                stock.save()

        if self.warehouse_to.stock_management:
            # for each position in the stock list, update the warehouse stock
            for pos in StockListPosition.objects.filter(stocklist=self.stocklist.id):
                stock, created = Stock.objects.update_or_create(
                    product=pos.product,
                    warehouse=self.warehouse_to
                )
                stock.amount -= pos.amount
                stock.save()

        sc = StockChange.objects.filter(stocktransfer=self)
        sc.delete()
        self.booked = False
        self.save()
        return True

    def __unicode__(self):
        return u"{}: {} nach {}".format(self.date, self.warehouse_from, self.warehouse_to)

    class Meta:
        ordering = ['-date']


class StockTransferListPos(StockListPos):
    stocktransfer = models.ForeignKey(StockTransfer)

    class Meta:
        unique_together = (("stocktransfer", "product"),)

class Invoice(models.Model):
    """
    """
    from_org = models.ForeignKey(Organisation, related_name='invoice_from')
    to_org = models.ForeignKey(Organisation, related_name='invoice_to')
    comments = models.TextField(blank=True, null=True, verbose_name="Kommentare")
    purchaseorder = models.ForeignKey('PurchaseOrder', blank=True, null=True)
    salesorder = models.ForeignKey('SalesOrder', blank=True, null=True)
    history = HistoricalRecords()


class InvoiceListPos(StockListPos):
    """
    """
    invoice = models.ForeignKey(Invoice)

    class Meta:
        unique_together = (("invoice", "product"),)


class PurchaseOrder(StockListPos):
    """
    PurchaseOrders represent orders from the issueing organisation to another (procurement).
    TODO:
    - states
    - methods:
        - create invoice
        - create procurement (stock in)
        - mark as paid
    """
    to = models.ForeignKey(Organisation)
    comments = models.TextField(blank=True, null=True, verbose_name="Kommentare")
    history = HistoricalRecords()

    # ride = models.ForeignKey(Ride, blank=True, null=True)
    

class PurchaseOrderListPos(StockListPos):
    """
    """
    purchaseorder = models.ForeignKey(PurchaseOrder)

    def __unicode__(self):
        return u"PurchaseOrder #{}: {}x {} ".format(self.purchoseorder.id, self.amount, self.product)
        
    class Meta:
        unique_together = (("purchaseorder", "product"),)


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
    to = models.ForeignKey(Organisation)
    comments = models.TextField(blank=True, null=True, verbose_name="Kommentare")
    history = HistoricalRecords()

    # container = models.ForeignKey(Container)

class SalesOrderListPos(StockListPos):
    """
    """
    salesorder = models.ForeignKey(SalesOrder)

    def __unicode__(self):
        return u"PurchaseOrder #{}: {}x {} ".format(self.purchoseorder.id, self.amount, self.product)
        
    class Meta:
        unique_together = (("salesorder", "product"),)


class PartnerSud(models.Model):
    """
    Represents a partner of the Velafrica Sud Network.
    """
    organisation = models.ForeignKey(Organisation)
    image = ResizedImageField(storage=fs, size=[800, 800], upload_to='velafrica_sud/partner/', blank=True, null=True, help_text='Foto vom Partner vor Ort.')

    org_form = models.CharField(max_length=255, blank=True, null=True)
    legalform = models.CharField(max_length=255, blank=True, null=True, verbose_name="Organisationsform")
    partner_since = models.IntegerField(blank=True, null=True, verbose_name="Partner seit...", help_text="Jahr")
    vocational_training = models.BooleanField(default=False, verbose_name="Bietet Berufsbildung an")
    infrastructure = models.TextField(verbose_name="Infrastruktur", help_text="Übersicht über die Infrastruktur vor Ort (Anzahl Arbeitsplätze, Lagermöglichkeiten, Art der Gebäude etc)", blank=True, null=True)

    history = HistoricalRecords()

    def get_container_count(self):
        return Container.objects.filter(partner_to=self).count()
    get_container_count.short_description = 'Anzahl exp. Container'

    def get_bicycle_count(self):
        count = 0
        for c in Container.objects.filter(partner_to=self):
            count += c.velos_loaded
        return count
    get_bicycle_count.short_description = 'Anzahl exp. Velos'

    def __unicode__(self):
        return u"{}, {}".format(self.organisation.name, self.organisation.address.country)

    class Meta:
        ordering = ['organisation__name']
        verbose_name_plural = "Partner Süd"
