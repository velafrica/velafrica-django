# -*- coding: utf-8 -*-
from datetime import datetime
from django.core.validators import RegexValidator, EmailValidator
from django.db import models
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords
from velafrica.organisation.models import Organisation
from velafrica.velafrica_sud.models import PartnerSud, Container


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

class TrackingEvent(models.Model):
    """

    """

    EVENT_TYPE_CHOICES = (
        ('initial', 'Tracking erstellt'),
        ('vpn_in', 'Eingang VPN'),
        ('workshop_in', 'Eingang Werkstatt'),
        ('ready_for_export', 'Bereit für Export'),
        ('load_container', 'Containerverlad'),
        ('arrival', 'Ankunft Partner Süd')
    )

    datetime = models.DateTimeField(blank=False, null=False, default=datetime.now, verbose_name="Zeitpunkt")
    event_type = models.CharField(
        choices=EVENT_TYPE_CHOICES, 
        default='initial',
        max_length=255, 
        help_text="Art des Events"
        )
    tracking = models.ForeignKey(Tracking)
    note = models.CharField(blank=True, null=True, max_length=255, verbose_name="Bemerkung")
    history = HistoricalRecords()

    class Meta:
        ordering = ['-datetime']
