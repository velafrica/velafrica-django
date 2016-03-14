# -*- coding: utf-8 -*-
from datetime import datetime
from django.core.validators import RegexValidator, EmailValidator
from django.db import models
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords


class Tracking(models.Model):
    """
    Represents one bicycle that is being tracked.
    """
    trackingno = models.CharField(blank=False, null=False, max_length=10, unique=True, verbose_name="Tracking Nummer")

    number_of_velos = models.IntegerField(blank=False, null=False, default=0)

    first_name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Vorname")
    last_name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Nachname")
    street = models.CharField(blank=True, null=True, max_length=255, verbose_name="Strasse")
    plz = models.IntegerField(blank=True, null=True, verbose_name="Postleitzahl")
    town = models.CharField(blank=False, null=False, max_length=255, verbose_name="Stadt")
    email = models.CharField(blank=False, null=False, max_length=255, verbose_name="Email", validators=[EmailValidator])
    tel = models.CharField(blank=False, null=False, max_length=255, verbose_name="Telefonnummer")

    history = HistoricalRecords()

    def get_last_event(self):
        return null

    def __unicode__(self):
        return u"#{}: {} {}, {} Velos".format(self.trackingno, self.first_name, self.last_name, self.number_of_velos)

    class Meta:
        ordering = ['-trackingno']


class TrackingEventState(models.Model):
    """

    """
    name = models.CharField(blank=True, null=True, max_length=255, verbose_name="Name")
    description = models.CharField(blank=True, null=True, max_length=255, verbose_name="Beschreibung")
    history = HistoricalRecords()


class TrackingEvent(models.Model):
    """

    """
    datetime = models.DateTimeField(blank=False, null=False, default=datetime.now, verbose_name="Zeitpunkt")
    # location =
    state = models.ForeignKey(TrackingEventState)
    tracking = models.ForeignKey(Tracking)
    note = models.CharField(blank=True, null=True, max_length=255, verbose_name="Bemerkung")
    history = HistoricalRecords()

    class Meta:
        ordering = ['-datetime']
