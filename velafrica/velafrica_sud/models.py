# -*- coding: utf-8 -*-
from datetime import datetime
from django.core.validators import RegexValidator
from django.db import models
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords
from velafrica.organisation.models import Organisation


class Country(models.Model):
    """
    Represents a country of the world.
    """
    name = models.CharField(blank=False, null=True, max_length=255, verbose_name="Name des Landes")
    flag = ResizedImageField(size=[500, 500], upload_to='velafrica_sud/country/flags/', blank=True, null=True, help_text='Flagge des Landes.')

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        ordering = ['-name']
        verbose_name_plural = "Countries"


class PartnerSud(models.Model):
    """
    Represents a partner of the Velafrica Sud Network.
    """
    name = models.CharField(blank=False, null=True, max_length=255, verbose_name="Name der Organisation")
    latitude = models.IntegerField(blank=True, null=True, verbose_name='Breitengrad')
    longitude = models.IntegerField(blank=True, null=True, verbose_name='Längengrad')
    country = models.ForeignKey(Country, verbose_name='Land')
    website = models.CharField(blank=True, null=True, max_length=255, verbose_name="Website")

    history = HistoricalRecords()

    def __unicode__(self):
        return u"{}, {}".format(self.name, self.country)

    class Meta:
        ordering = ['name']


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
    partner_to = models.ForeignKey(PartnerSud, blank=False, null=False, verbose_name='Destination')

    velos = models.IntegerField(blank=False, null=False, default=0, verbose_name='Anzahl Velos')
    spare_parts = models.BooleanField(default=False, verbose_name='Ersatzteile transportiert?')

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

    def __unicode__(self):
        return u"Container {} to {}".format(self.container_no, self.partner_to)

    class Meta:
        ordering = ['-pickup_date']
