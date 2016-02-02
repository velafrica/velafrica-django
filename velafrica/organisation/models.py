# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords

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
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Name der Organisation")
    street = models.CharField(blank=False, null=False, max_length=255, verbose_name="Strasse")
    plz = models.IntegerField(blank=False, null=False, verbose_name="PLZ")
    city = models.CharField(blank=False, null=False, max_length=255, verbose_name="Ort")

    website = models.CharField(blank=True, null=True, max_length=255, verbose_name="Website")

    history = HistoricalRecords()

    def __unicode__(self):
        return u"{}, {}".format(self.name, self.city)

    class Meta:
        ordering = ['name']

class Person(models.Model):
    """
    Person working at a network partner.
    """
    user = models.ForeignKey(User, verbose_name="Django User Account")
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
