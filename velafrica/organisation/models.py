# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.conf import settings
from django.db import models
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords
from velafrica.core import utils

class Canton(models.Model):
    """
    deprecated

    TODO: delete
    """
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Name des Kantons")
    short = models.CharField(blank=False, null=False, max_length=2, unique=True, verbose_name="Kürzel der Gemeinde")
    
    def __unicode__(self):
        return u"{} {}".format(self.name, self.short)


class Municipality(models.Model):
    """
    deprecated

    TODO: delete
    """
    gdenr = models.IntegerField(blank=False, null=False, verbose_name="Gemeindenr. des BFS")
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Name der Gemeinde")
    name_short = models.CharField(blank=False, null=False, max_length=255, verbose_name="Name der Gemeinde (kurz)")
    plz = models.IntegerField(blank=False, null=False, verbose_name="Postleitzahl")
    plz_name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Name der Gemeinde (Post)")
    canton = models.ForeignKey(Canton)

    def __unicode__(self):
        return u"{} {} ({})".format(self.plz, self.name, self.name_short)

    class Meta:
        verbose_name_plural = "Municipalities"


class Country(models.Model):
    """
    Represents a country of the world.
    """
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Name des Landes", unique=True)
    code = models.CharField(blank=True, null=True, max_length=255, verbose_name="Ländercode (ISO 3166-1 alpha-2)", unique=True)

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        ordering = ['-name']
        verbose_name_plural = "Countries"


class Address(models.Model):
    """
    Represents the address of an organisation / partner / warehouse.

    :model:`organisation.Country`
    """
    street = models.CharField(blank=True, null=True, max_length=255, verbose_name="Strasse und Hausnummer")
    zipcode = models.IntegerField(blank=True, null=True, verbose_name="Zipcode / PLZ")
    city = models.CharField(blank=True, null=True, max_length=255, verbose_name="Ort")
    state = models.CharField(blank=True, null=True, max_length=255, verbose_name="Kanton / Region")
    country = models.ForeignKey(Country, verbose_name="Land")

    latitude = models.DecimalField(blank=True, null=True, verbose_name='Breitengrad', max_digits=9, decimal_places=6)
    longitude = models.DecimalField(blank=True, null=True, verbose_name='Längengrad', max_digits=9, decimal_places=6)

    def get_geolocation(self):
        """
        """
        loc = utils.get_geolocation(self.__unicode__())
        if loc:
            self.latitude = loc['lat']
            self.longitude = loc['lng']
            self.save()
            return loc
        else:
            return None

    def __unicode__(self):
        return u"{}, {} {}, {}".format(self.street, self.zipcode, self.city, self.country)

    class Meta:
        verbose_name_plural = "Addresses"

class Organisation(models.Model):
    """
    Represents a network partner.
    
    Both Swiss and African partners are represented as organisations.

    African partners do have a linked :model:`velafrica_sud.PartnerSud` instance.
    """

    name = models.CharField(blank=False, null=True, max_length=255, verbose_name="Name der Organisation")
    website = models.URLField(blank=True, null=True, max_length=255, verbose_name="Website")
    address = models.ForeignKey(Address, verbose_name="Adresse", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contact = models.TextField(verbose_name="Kontaktperson", help_text="Name, Email, Telefon, Skype etc", blank=True, null=True)

    history = HistoricalRecords()

    def is_partnersud(self):
        """
        """
        if self.partnersud:
            return True
        else:
            return False
    is_partnersud.short_description = "Süd Partner"

    def get_partnersud(self):
        """
        """
        if self.partnersud:
            return self.partnersud
        else:
            return "-"
    get_partnersud.short_description = "Süd Partner"

    def __unicode__(self):
        if self.address:
            return u"{}, {}".format(self.name, self.address.city)
        else:
            return u"{}".format(self.name)

    class Meta:
        ordering = ['name']


class Person(models.Model):
    """
    Person working at a network partner.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Django User Account"
        )
    organisation = models.ForeignKey('Organisation', verbose_name="Arbeitgeber")

    def __unicode__(self):
        if (len(self.user.first_name) > 0 and len(self.user.last_name) > 0):
            return u"{} {} ({})".format(self.user.first_name, self.user.last_name, self.organisation.name)
        else:
            return u"{} ({})".format(self.user.username, self.organisation.name)

    class Meta:
        verbose_name_plural = "People"
