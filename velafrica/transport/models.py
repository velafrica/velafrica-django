# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords

from velafrica.core import utils
from velafrica.organisation.models import Organisation
from velafrica.stock.models import Warehouse, StockList


class Car(models.Model):
    """
    Represents a car.
    """
    name = models.CharField(blank=False, null=True, max_length=255, verbose_name="Name des Fahrzeugs")
    organisation = models.ForeignKey(Organisation, blank=True, null=True, help_text='Organisation welcher das Fahrzeug gehört.')
    image = ResizedImageField(size=[500, 500], upload_to='stock/categories/', blank=True, null=True, help_text='Foto des Fahrzeugs')
    plate = models.CharField(blank=True, null=True, max_length=255, verbose_name='Autokennzeichen')
    
    history = HistoricalRecords()

    def __str__(self):
        return u"{}".format(self.name)

    class Meta:
        ordering = ['name']


class Driver(models.Model):
    """
    Represents a driver.
    """
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Name des Fahrers")
    organisation = models.ForeignKey(Organisation, blank=True, null=True, help_text='Organisation bei welcher der Fahrer angestellt ist.')
    active = models.BooleanField(default=True, help_text='Ist der Fahrer noch bei Velafrica? Inaktive Fahrer werden als (inaktiv) in der Auswahl bei den Fahrten aufgeführtgi.')

    history = HistoricalRecords()
    
    def __str__(self):
        if not self.active:
            return u"{} (inaktiv)".format(self.name)
        return u"{}".format(self.name)

    class Meta:
        ordering = ['name']


class VeloState(models.Model):
    """
    Represents the state of a bicycle.
    """
    name = models.CharField(blank=False, null=False, max_length=40, verbose_name="Name des Zustandes")
    description = models.CharField(blank=True, null=True, max_length=255, verbose_name="Beschreibung")
    
    history = HistoricalRecords()

    def __str__(self):
        return u"{}".format(self.name)

    class Meta:
        ordering = ['name']


class Ride(models.Model):
    """
    Represents a ride from one destination to the other.
    Used to count how many bicycles went from one place to another in a certain period of time.

    :model:`stock.StockList`
    """
    date = models.DateField(blank=False, null=False, default=timezone.now, verbose_name="Datum")
    from_warehouse = models.ForeignKey(Warehouse, verbose_name='Start', related_name='from_warehouse', help_text='Start der Fahrt')
    from_warehouse_detail_address = models.TextField(blank=True, null=True,
                                                   verbose_name='FROM_WAREHOUSE alternative Adress (optional)',
                                                   help_text='Bei Auswahl von "Diverse Spender" als Startpunkt, kann hier optional die genaue Adresse eingetragen werden.')
    to_warehouse = models.ForeignKey(Warehouse, verbose_name='Ziel', related_name='to_warehouse', help_text='Ziel der Fahrt')
    to_warehouse_detail_address = models.TextField(blank=True, null=True,
                                                   verbose_name='TO_WAREHOUSE alternative Adress (optional)',
                                                   help_text='Bei Auswahl von "Diverse Spender" als Ziel, kann hier optional die genaue Adresse eingetragen werden.')
    driver = models.ForeignKey(Driver, verbose_name='Fahrer', help_text='Person die den Transport durchgeführt hat.')
    car = models.ForeignKey(Car, verbose_name='Fahrzeug')
    velos = models.IntegerField(blank=False, null=False, default=0, verbose_name='Anzahl Velos')
    velo_state = models.ForeignKey(VeloState, verbose_name='Zustand der Velos')
    spare_parts = models.BooleanField(default=False, verbose_name='Ersatzteile transportiert?')
    stocklist = models.OneToOneField(StockList, null=True, blank=True)
    note = models.CharField(blank=True, null=True, max_length=255, verbose_name="Bemerkung", help_text="Bemerkung zur Fahrt")
    
    distance = models.IntegerField(verbose_name="Ungefähre Distanz in Meter", blank=True, null=True)

    history = HistoricalRecords()

    def get_distance(self):
        """
        Get distance from start to end of the driven way, using the Google Maps API.
        """
        loc1 = self.from_warehouse.get_geolocation()
        loc2 = self.to_warehouse.get_geolocation()
        if loc1 and loc2:
            result = utils.get_distance(loc1, loc2)
            if type(result) == int:
                self.distance = result
                self.save()
                return result
        return None

    def get_googlemaps_url(self):
        """
        """
        start = self.from_warehouse.get_address()
        end = self.to_warehouse.get_address()
        if start and end:
            if start.city and start.country and end.city and end.country:
                return utils.get_googlemaps_url_distance(self.from_warehouse.get_address(), self.to_warehouse.get_address())
        return None


    def __str__(self):
        try:
            return u"Fahrt {}, {}: {} nach {}".format(self.id, self.date, self.from_warehouse, self.to_warehouse)
        except:
            return u"Fahrt {}".format(self.id)

    class Meta:
        ordering = ['-date', 'from_warehouse']
