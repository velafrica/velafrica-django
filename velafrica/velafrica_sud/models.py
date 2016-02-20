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


class PartnerSud(models.Model):
    """
    Represents a partner of the Velafrica Sud Network.
    """
    name = models.CharField(blank=False, null=True, max_length=255, verbose_name="Name der Organisation")
    street = models.CharField(blank=True, null=True, max_length=255, verbose_name="Strasse")
    plz = models.IntegerField(blank=True, null=True, verbose_name="PLZ")
    city = models.CharField(blank=True, null=True, max_length=255, verbose_name="Ort")
    country = models.ForeignKey(Country, verbose_name='Land')
    website = models.CharField(blank=True, null=True, max_length=255, verbose_name="Website")

    history = HistoricalRecords()

    def __unicode__(self):
        return u"{}, {}".format(self.name, self.country)

    class Meta:
        ordering = ['name']


class Container(models.Model):
    """
    Represents a container.
    """
    organisation_from = models.ForeignKey(Organisation, blank=True, null=True, help_text='Organisation welcher das Fahrzeug gehört.')
    pickup_date = models.DateField(blank=False, null=False)
    partner_to = models.ForeignKey(PartnerSud, blank=False, null=False)
    arrival_date = models.DateField()    
    container_no = models.CharField(blank=True, null=True, max_length=255, verbose_name='Container Nummer')
    sealing_no = models.CharField(blank=True, null=True, max_length=255, verbose_name='Container Nummer')
    velos = models.IntegerField(blank=False, null=False, default=0, verbose_name='Anzahl Velos')
    spare_parts = models.BooleanField(default=False, verbose_name='Ersatzteile transportiert?')
    notes = models.TextField(blank=True, null=True, verbose_name="Bemerkungen zum Container")
    history = HistoricalRecords()

    def __unicode__(self):
        return u"Container {} to {}".format(self.container_no, self.partner_to)

    class Meta:
        ordering = ['-pickup_date']
