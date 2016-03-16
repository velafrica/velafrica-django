# -*- coding: utf-8 -*-
from datetime import datetime
from django.core.validators import RegexValidator
from django.db import models
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords
from velafrica.organisation.models import Person, Organisation

class Category(models.Model):
    """
    Represents a product category.
    """
    articlenr_start = models.CharField(blank=True, null=True, max_length=8, verbose_name="Kategorienummer", unique=True, help_text="")
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Kategoriebezeichnung")
    description = models.TextField(blank=True, null=True, verbose_name="Beschreibung")
    image = ResizedImageField(size=[500, 500], upload_to='stock/categories/', blank=True, null=True, help_text='Product picture.')
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
    hscode = models.CharField(blank=False, null=False, max_length=7, verbose_name="Harmonized System Code")
    description = models.TextField(blank=True, null=True, verbose_name="Beschreibung", help_text="Hinweise zur Qualität bzw Hinweise und Ergänzung")
    category = models.ForeignKey('Category', verbose_name="Kategorie", help_text='Die Hauptkategorie des Produktes.')
    image = ResizedImageField(size=[500, 500], upload_to='stock/products/', blank=True, null=True, verbose_name="Produktbild")
    price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    history = HistoricalRecords()

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
    image = ResizedImageField(size=[500, 500], upload_to='stock/warehouses/', blank=True, null=True, verbose_name="Bild des Lagers")
    stock_management = models.BooleanField(default=False, verbose_name="Automatisches Stock-Management", help_text="Gibt an ob automatisches Stock-Management aktiviert ist, d.h. ob bei Stock Verschiebungen der Stock automatisch angepasst werden soll.")
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


class StockList(models.Model):
    """
    A StockList is an universal object that can be used in various contexts,
    like as a payload inventory of a container or a transport, or as an inventory
    of an internal stock transfer.
    """
    last_change = models.DateTimeField(default=datetime.now)
    description = models.CharField(blank=True, null=True, max_length=255)
    history = HistoricalRecords()

    def __unicode__(self):
        return u"StockList {}, {}".format(self.last_change, self.description)


class StockListPosition(models.Model):
    """
    One position in a StockList.
    """
    stocklist = models.ForeignKey(StockList, verbose_name='StockList')
    product = models.ForeignKey(Product)
    amount = models.IntegerField(blank=False, null=False, verbose_name="Stückzahl")
    history = HistoricalRecords()

    class Meta:
        unique_together = (("stocklist", "product"),)

    def __unicode__(self):
        return u"{}: {} in {}".format(self.product, self.amount, self.stocklist)


class StockTransfer(models.Model):
    """
    A StockTransfer object represents the moving of a stock from one warehouse to another.
    It can bee 'booked', which creates a new StockChange object for the 'from' and the 'to' warehouse
    and sets self.booked to True. The StockChange will get a deep copy of the StockList.
    Revoking a StockTransfer will delete the StockChange objects and reset
    self.booked to False.    
    """
    date = models.DateField(blank=False, null=False, default=datetime.now, verbose_name="Ausführdatum")
    warehouse_from = models.ForeignKey(Warehouse, related_name="warehouse_from", verbose_name="Herkunfts-Lager")
    warehouse_to = models.ForeignKey(Warehouse, related_name="warehouse_to", verbose_name="Ziel-Lager")
    stocklist = models.ForeignKey(StockList, verbose_name="Stock List")
    note = models.CharField(blank=True, null=True, max_length=255, verbose_name="Bemerkungen")
    booked = models.BooleanField(default=False, null=False, blank=False, help_text="Gibt an ob der Stock bereits angepasst wurde.")
    history = HistoricalRecords()

    def __unicode__(self):
        return u"{}: {} nach {}".format(self.date, self.warehouse_from, self.warehouse_to)

    class Meta:
        ordering = ['-date']


class StockChange(models.Model):
    """
    StockChange objects are used to keep track of all the stock changes per warehouse.
    StockChange objects never get created by the user directly, but when booking a StockTransfer.
    On pre_save, the application checks on the warehouse if stock is managed automatically.
    If so, the stock for all the objects in the StockList will be adjusted depending on the stock change type.
    On pre_delete, the application undoes the stock changes and then deletes the StocChange object.
    """
    STOCK_CHANGE_TYPES = {
        ('in', 'in'),
        ('out', 'out')
    }
    datetime = models.DateTimeField(default=datetime.now)
    stocktransfer = models.ForeignKey(StockTransfer)
    warehouse = models.ForeignKey(Warehouse)
    stocklist = models.ForeignKey(StockList)
    stock_change_type = models.CharField(choices=STOCK_CHANGE_TYPES, max_length=255)

    def __unicode__(self):
        return u"StockChange {}, {} {}".format(self.datetime, self.stock_change_type, self.warehouse)
