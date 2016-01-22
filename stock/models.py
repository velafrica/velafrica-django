from django.db import models
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords


class Category(models.Model):
    """
    Represents a product category.
    """
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Kategoriebezeichnung")
    description = models.TextField(blank=True, null=True, verbose_name="Beschreibung")
    image = models.ImageField()
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
    category = models.ForeignKey(Category, verbose_name="Category", related_name='category')
    image = ResizedImageField(size=[500, 500], upload_to='stock/img/', blank=True, null=True, help_text='Product picture.')
    history = HistoricalRecords()

    def __unicode__(self):
        return "{}: {}".format(self.sku, self.name)

    class Meta:
        ordering = ['sku']
