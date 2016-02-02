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
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Kategoriebezeichnung")
    description = models.TextField(blank=True, null=True, verbose_name="Beschreibung")
    image = ResizedImageField(size=[500, 500], upload_to='stock/categories/', blank=True, null=True, help_text='Product picture.')
    articlenr_start = models.CharField(blank=True, null=True, max_length=7, verbose_name="Erste Nummer des Artikelnummerbereiches", unique=True, help_text="")
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
        ordering = ['name']


class Product(models.Model):
    """
    Represents a product.
    """
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Produktbezeichnung")
    articlenr = models.CharField(blank=False, null=False, default="000.000", max_length=7, verbose_name="Artikelnummer", unique=True, help_text="Die Velafrica Artikelnummer (in der Form 123.123)")
    hscode = models.CharField(blank=False, null=False, default="0000.00", max_length=7, verbose_name="Harmonized System Code")
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
    organisation = models.ForeignKey(Organisation, verbose_name="Lager", help_text='Die Organisation zu welcher das Lager gehört.')
    image = ResizedImageField(size=[500, 500], upload_to='stock/warehouses/', blank=True, null=True, verbose_name="Bild des Lagers")
    
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
    
    def __unicode__(self):
        return u"{}: {} x {}".format(self.warehouse.name, self.amount, self.product.name)

    class Meta:
        ordering = ['warehouse', 'product']


class StockTransfer(models.Model):
    """
    Used for every inhouse stock movement
    TODO: everything
    - date
    - from
    - to
    - products + amount
    - executor
    - state (draft / booked)
    """
    executor = models.ForeignKey(Person, null=False, blank=False, verbose_name="Ausführende Person", help_text="Die Person welche die Verschiebung vorgenommen hat.")
    date = models.DateField(blank=False, null=False, default=datetime.now, verbose_name="Ausführdatum")
    booked = models.BooleanField(default=False, null=False, blank=False, help_text="Gibt an ob der Stock bereits angepasst wurde.")
    warehouse_from = models.ForeignKey(Warehouse, related_name="warehouse_from")
    warehouse_to = models.ForeignKey(Warehouse, related_name="warehouse_to")

    def __unicode__(self):
        return u"{}: {} nach {}".format(self.date, self.warehouse_from, self.warehouse_to)

    class Meta:
        ordering = ['-date']

class StockTransferPosition(models.Model):
    """
    One position in a StockTransfer.
    """
    stocktransfer = models.ForeignKey(StockTransfer, verbose_name='Der zugehörige StockTransfer')
    product = models.ForeignKey(Product)
    amount = models.IntegerField(blank=False, null=False, verbose_name="Stückzahl")
