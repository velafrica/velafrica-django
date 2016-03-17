# -*- coding: utf-8 -*-
from datetime import datetime
from django.core.validators import RegexValidator, EmailValidator
from django.db import models
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords
from velafrica.organisation.models import Organisation
from velafrica.velafrica_sud.models import PartnerSud, Container

from velafrica.core.ftp import MyFTPStorage
fs = MyFTPStorage()

class Tracking(models.Model):
    """
    Represents one bicycle that is being tracked.
    """
    tracking_no = models.CharField(blank=False, null=False, max_length=10, unique=True, verbose_name="Tracking Nummer")

    number_of_velos = models.IntegerField(blank=False, null=False, default=0, verbose_name="Anzahl Velos")

    vpn = models.ForeignKey(Organisation, 
        null=True, 
        blank=True, 
        verbose_name="Partner", 
        help_text="wird momentan noch nicht berücksichtigt"
    )
    destination = models.ForeignKey(PartnerSud, null=True, blank=True, verbose_name="Destination")

    first_name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Vorname")
    last_name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Nachname")
    email = models.CharField(blank=False, null=False, max_length=255, verbose_name="Email", validators=[EmailValidator])

    container = models.ForeignKey(Container, blank=True, null=True)
    ready_for_export = models.BooleanField(blank=False, null=False, default=False, verbose_name="Velo ist exportbereit")
    completed = models.BooleanField(blank=False, null=False, default=False, verbose_name="Velo ist in Afrika angekommen")

    history = HistoricalRecords()

    def get_last_event(self):
        return null

    def __unicode__(self):
        return u"#{}: {} {}, {} Velos".format(self.tracking_no, self.first_name, self.last_name, self.number_of_velos)

    class Meta:
        ordering = ['-tracking_no']


class TrackingEventType(models.Model):
    """
    Tracking event types, recommended:

    1. Tracking erstellt
    2. Eingang Velafrica
    3. Eingang Velowerkstatt
    5. Bereit für Export
    4. Containerverlad
    5. Ankunft Partner in Afrika

    """
    name = models.CharField(blank=False, null=False, max_length=255)
    description = models.CharField(blank=True, null=True, max_length=255)
    send_email = models.BooleanField(
        blank=False, 
        null=False, 
        help_text="Aktivieren falls bei Erstellung eines Events dieser Art automatisch ein Email an den Spender versandt werden soll."
    )
    history = HistoricalRecords()

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        ordering = ['name']


class TrackingEvent(models.Model):
    """
    Represents an event during tracking of a bicycle.
    """
    datetime = models.DateTimeField(blank=False, null=False, default=datetime.now, verbose_name="Zeitpunkt")
    event_type = models.ForeignKey(TrackingEventType, help_text="Art des Events")
    tracking = models.ForeignKey(Tracking)
    note = models.CharField(blank=True, null=True, max_length=255, verbose_name="Bemerkung")
    history = HistoricalRecords()

    class Meta:
        ordering = ['-datetime']


class EmailLog(models.Model):
    """
    """
    tracking = models.ForeignKey(Tracking)
    tracking_event = models.ForeignKey(TrackingEvent)
    subject = models.CharField(blank=False, null=False, max_length=255)
    sender = models.CharField(blank=False, null=False, max_length=255)
    receiver = models.CharField(blank=False, null=False, max_length=255)
    datetime = models.DateTimeField(blank=False, null=False, default=datetime.now)
    message = models.TextField(blank=True, null=True)
    history = HistoricalRecords()
