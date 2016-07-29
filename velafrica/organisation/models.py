# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.conf import settings
from django.db import models
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords

class Canton(models.Model):
    """
    TODO: delete
    """
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Name des Kantons")
    short = models.CharField(blank=False, null=False, max_length=2, unique=True, verbose_name="Kürzel der Gemeinde")
    
    def __unicode__(self):
        return u"{} {}".format(self.name, self.short)


class Municipality(models.Model):
    """
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
    """
    street = models.CharField(blank=True, null=True, max_length=255, verbose_name="Strasse und Hausnummer")
    zipcode = models.IntegerField(blank=True, null=True, verbose_name="Zipcode / PLZ")
    city = models.CharField(blank=False, null=False, max_length=255, verbose_name="Ort")
    state = models.CharField(blank=True, null=True, max_length=255, verbose_name="Kanton / Region")
    country = models.ForeignKey(Country, verbose_name="Land")

    latitude = models.DecimalField(blank=True, null=True, verbose_name='Breitengrad', max_digits=9, decimal_places=6)
    longitude = models.DecimalField(blank=True, null=True, verbose_name='Längengrad', max_digits=9, decimal_places=6)

    def __unicode__(self):
        return u"{}, {} {}, {}".format(self.street, self.zipcode, self.city, self.country)

    class Meta:
        verbose_name_plural = "Addresses"

class Organisation(models.Model):
    """
    Represents a network partner.
    TODO:
    - differentiate between org types (string rep, admin)
    """

    # general information
    name = models.CharField(blank=False, null=True, max_length=255, verbose_name="Name der Organisation")
    website = models.URLField(blank=True, null=True, max_length=255, verbose_name="Website")
    address = models.ForeignKey(Address, verbose_name="Adresse", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contact = models.TextField(verbose_name="Kontaktperson", help_text="Name, Email, Telefon, Skype etc", blank=True, null=True)


    # TODO: following fields will be removed in the future
    street = models.CharField(blank=True, null=True, max_length=255, verbose_name="Strasse", help_text="WARNING: Will be removed soon") 
    plz = models.IntegerField(blank=True, null=True, verbose_name="PLZ", help_text="WARNING: Will be removed soon")
    city = models.CharField(blank=True, null=True, max_length=255, verbose_name="Ort", help_text="WARNING: Will be removed soon")

    history = HistoricalRecords()
    
    def migrate_address(self):
        """
        Create address from deprecated fields
        """
        if not self.address:
            c, created = Country.objects.get_or_create(code="ch", name="Schweiz")
            a =  Address(
                    street = self.street,
                    zipcode = self.plz,
                    city = self.city,
                    country = c
                )
            a.save()
            self.address = a
            self.save()

    def has_partnersud(self):
        if self.partnersud:
            return True
        else:
            return False

    def __unicode__(self):
        return u"{}, {}".format(self.name, self.city)

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
    #first_name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Vorname")
    #last_name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Nachname")
    organisation = models.ForeignKey('Organisation', verbose_name="Arbeitgeber")

    def __unicode__(self):
        if (len(self.user.first_name) > 0 and len(self.user.last_name) > 0):
            return u"{} {} ({})".format(self.user.first_name, self.user.last_name, self.organisation.name)
        else:
            return u"{} ({})".format(self.user.username, self.organisation.name)

    class Meta:
        verbose_name_plural = "People"
