# -*- coding: utf-8 -*-
from django.core.validators import RegexValidator
from django.db import models
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords
from velafrica.organisation.models import Organisation
from velafrica.stock.models import StockList
from velafrica.core.ftp import MyFTPStorage
fs = MyFTPStorage()

class Country(models.Model):
    """
    Represents a country of the world.
    """
    name = models.CharField(blank=False, null=True, max_length=255, verbose_name="Name des Landes")
    flag = ResizedImageField(storage=fs, size=[500, 500], upload_to='velafrica_sud/country/flags/', blank=True, null=True, help_text='Flagge des Landes.')

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        ordering = ['-name']
        verbose_name_plural = "Countries"


class Forwarder(models.Model):
    """
    Represents a logistics partner.
    """
    name = models.CharField(blank=False, null=True, max_length=255, verbose_name="Name des Forwarders")

    history = HistoricalRecords()

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        ordering = ['name']


class Container(models.Model):
    """
    Represents a container.
    """
    organisation_from = models.ForeignKey(Organisation, blank=True, null=True, verbose_name='Verarbeitungspartner', help_text='Ort wo der Container geladen wurde.')
    partner_to = models.ForeignKey('PartnerSud', blank=False, null=False, verbose_name='Destination')

    velos_loaded = models.IntegerField(blank=False, null=False, default=0, verbose_name='Anzahl Velos eingeladen')
    velos_unloaded = models.IntegerField(blank=False, null=False, default=0, verbose_name='Anzahl Velos ausgeladen')
    spare_parts = models.BooleanField(default=False, verbose_name='Ersatzteile transportiert?')
    stocklist = models.OneToOneField(StockList, null=True, blank=True)

    velos_worth = models.IntegerField(blank=False, null=False, default=0, verbose_name='Wert der Velos')   
    spare_parts_worth = models.IntegerField(blank=False, null=False, default=0, verbose_name='Wert der Ersatzteile')
    tools_worth = models.IntegerField(blank=False, null=False, default=0, verbose_name='Wert der Ersatzteile')
    various_worth = models.IntegerField(blank=False, null=False, default=0, verbose_name='Wert der Ersatzteile')
    
    pickup_date = models.DateField(blank=False, null=False, verbose_name='Ladedatum')
    shipment_date = models.DateField(blank=True, null=True, verbose_name='Verschiffungsdatum ab Europa') 
    arrival_port_date = models.DateField(blank=True, null=True, verbose_name='Ankunft Hafen Partner')
    arrival_partner_date = models.DateField(blank=True, null=True, verbose_name='Ankunft Partner')
    logistics = models.ForeignKey(Forwarder, blank=True, null=True, max_length=255, verbose_name='Forwarder', help_text='Logistikunternehmen')

    container_no = models.CharField(blank=True, null=True, max_length=255, verbose_name='Containernummer')
    seal_no = models.CharField(blank=True, null=True, max_length=255, verbose_name='Plombennummer')
    sgs_certified = models.BooleanField(default=False, verbose_name='SGS zertifiziert?')

    notes = models.TextField(blank=True, null=True, verbose_name="Bemerkungen zum Container")
    history = HistoricalRecords()

    def get_trimmed_container_no(self):
        if self.container_no:
            return self.container_no.replace(" ", "").replace("-", "")
        else:
            return None

    def __unicode__(self):
        return u"Container {} to {} ({})".format(self.container_no, self.partner_to, self.pickup_date)

    class Meta:
        ordering = ['-pickup_date']


class PartnerSud(models.Model):
    """
    Represents a partner of the Velafrica Sud Network.
    """
    name = models.CharField(blank=False, null=True, max_length=255, verbose_name="Name der Organisation")
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True, max_length=255, verbose_name="Website")

    street = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name='Land')
    latitude = models.DecimalField(blank=True, null=True, verbose_name='Breitengrad', max_digits=9, decimal_places=6)
    longitude = models.DecimalField(blank=True, null=True, verbose_name='Längengrad', max_digits=9, decimal_places=6)

    org_type = models.CharField(max_length=255, blank=True, null=True)
    legalform = models.CharField(max_length=255, blank=True, null=True, verbose_name="Organisationsform")
    partner_since = models.IntegerField(blank=True, null=True, verbose_name="Partner seit...", help_text="Jahr")
    

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
        return u"{}, {}".format(self.name, self.country)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Partner Süd"