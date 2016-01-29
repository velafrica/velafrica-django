from django.core.validators import RegexValidator
from django.db import models
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords

class Category(models.Model):
    """
    Represents a product category.
    """
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
        return "{}".format(self.name)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']


class Product(models.Model):
    """
    Represents a product category.
    """
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Produktbezeichnung")
    sku = models.CharField(blank=False, null=False, max_length=255, verbose_name="SKU", unique=True)
    description = models.TextField(blank=True, null=True, verbose_name="Beschreibung")
    category = models.ForeignKey('Category', verbose_name="Category")
    image = ResizedImageField(size=[500, 500], upload_to='stock/products/', blank=True, null=True, help_text='Product picture.')
    history = HistoricalRecords()

    def __unicode__(self):
        return "{}: {}".format(self.sku, self.name)

    class Meta:
        ordering = ['sku']


class Warehouse(models.Model):
    """
    TODO: everything
    - Name
    - Organisation
    - Adresse
    - Beschreibung
    """
    pass

class Stock(models.Model):
    """
    TODO: everything
    - Warehouse
    - Product
    - amount
    """
    pass


class StockMovement(models.Model):
    """
    Used for every inhouse stock movement
    TODO: everything
    - date
    - from
    - to
    - products + amount
    """
    pass

class StockInOut(models.Model):
    """
    Used for incoming and outgoing stock
    TODO: everything
    - date
    - type (in / out)
    - warehouse
    - note
    - products + amount
    """
    pass