# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.conf import settings
from django.db import models
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords

"""
class Adress(models.Model):

    municipality = ForeignKey(municipality)
    street 
    street_no
    country

"""

class Canton(models.Model):
    """
    """
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Name des Kantons")
    short = models.CharField(blank=False, null=False, max_length=2, unique=True, verbose_name="Kürzel der Gemeinde")
    
    def __unicode__(self):
        return u"{} {}".format(self.name, self.short)


class Municipality(models.Model):
    """
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


class Organisation(models.Model):
    """
    Represents a network partner.
    TODO:
    - name
    - Adresse
    - Kontaktperson (Vorname / Nachname)
    - Tel
    - Email
    - Bemerkungen
    - Website
    """
    name = models.CharField(blank=False, null=True, max_length=255, verbose_name="Name der Organisation")
    street = models.CharField(blank=True, null=True, max_length=255, verbose_name="Strasse")
    plz = models.IntegerField(blank=True, null=True, verbose_name="PLZ")
    city = models.CharField(blank=True, null=True, max_length=255, verbose_name="Ort")

    website = models.URLField(blank=True, null=True, max_length=255, verbose_name="Website")

    history = HistoricalRecords()

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
