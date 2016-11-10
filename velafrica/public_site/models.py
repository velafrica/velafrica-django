# -*- coding: utf-8 -*-
from django.db import models


class DonationAmount(models.Model):
    is_active = models.BooleanField(verbose_name='Aktiv', default=True)
    description = models.TextField(verbose_name='Beschreibung')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return u"{} - {}".format(self.amount, self.description[0:80])

    class Meta:
        verbose_name = 'Geldspendebetrag'
        verbose_name_plural = 'Geldspendebeträge'


class InvoiceOrder(models.Model):
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Betrag")
    empty_invoice = models.BooleanField(default=False, verbose_name="Leerer Einzahlungsschein")
    number_invoices = models.IntegerField(default=1, verbose_name="Menge")
    first_name = models.CharField(max_length=255, verbose_name="Vorname")
    last_name = models.CharField(max_length=255, verbose_name="Nachname")
    address = models.CharField(max_length=255, verbose_name="Adresse")
    zip = models.CharField(max_length=255, verbose_name="PLZ, Ort")
    comment = models.TextField(verbose_name="Anmerkung", blank=True)

    def __unicode__(self):
        return u"{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Einzahlungschein'
        verbose_name_plural = 'Einzahlungsscheine'


class WalkthroughRequest(models.Model):
    PERSON_TYPE_CHOICES = (
        (1, 'Verein'),
        (2, 'Firma'),
        (3, 'Gemeinde'),
        (4, 'Kirchgemeinde'),
        (5, 'Schule'),
        (6, 'Liegenschaftsverwaltung'),
        (7, 'Privatperson'),
        (8, 'Andere'),
    )
    EXPECTED_VELOS = (
        (1, '1 - 20'),
        (2, '21 - 50'),
        (3, '51 - 100'),
        (4, '101 - 1000'),
        (5, '> 1000'),
    )
    SUPPORTERS_COUNT = (
        (1, '1 - 10'),
        (2, '11 - 20'),
        (3, '21 - 30'),
        (4, '31 - 40'),
        (4, '41 - 50'),
    )

    first_name = models.CharField(max_length=255, verbose_name="Vorname")
    last_name = models.CharField(max_length=255, verbose_name="Nachname")
    phone = models.CharField(max_length=255, verbose_name="Telefonnummer")
    email = models.CharField(max_length=255, verbose_name="E-Mail")
    organizer_type = models.IntegerField(verbose_name="Aufstellung", choices=PERSON_TYPE_CHOICES, default=1)
    organizer_type_note = models.TextField(blank=True, verbose_name="Bemerkung")

    # optional/detail information
    date_start = models.DateField(blank=True, null=True, verbose_name="Datum von")
    date_end = models.DateField(blank=True, null=True, verbose_name="Datum bis")
    pickup_time_start = models.CharField(max_length=255, verbose_name="Annahmezeit von", blank=True)
    pickup_time_end = models.CharField(max_length=255, verbose_name="Annahmezeit bis", blank=True)
    address = models.CharField(max_length=255, verbose_name='Adresse', blank=True)
    zip = models.CharField(max_length=255, verbose_name="Postleitzahl", blank=True)
    address_note = models.TextField(verbose_name="Standortbeschreibung", blank=True)
    expected_velos = models.IntegerField(verbose_name="Erwartete Menge gesammelter Velos", choices=EXPECTED_VELOS, default=1)
    can_store = models.BooleanField(default=False, verbose_name="Kann Velos vor Ort zwischenlagern")
    can_deliver = models.BooleanField(default=False, verbose_name="Kann Abtransport zu Partner übernehmen")
    velafrica_pickup = models.BooleanField(default=False, verbose_name="Abtransport durch Velafrica")
    responsible_first_name = models.CharField(verbose_name="Vorname", max_length=255, blank=True)
    responsible_last_name = models.CharField(verbose_name="Nachname", max_length=255, blank=True)
    responsible_phone = models.CharField(verbose_name="Telefonnummer", max_length=255, blank=True)
    responsible_email = models.CharField(verbose_name="E-Mail", max_length=255, blank=True)
    supporter_count = models.IntegerField(verbose_name="Anzahl Helfer", choices=SUPPORTERS_COUNT, default=1)
    supporter_note = models.TextField(verbose_name="Bemerkung", blank=True)


    class Meta:
        verbose_name = 'Sammelanlassanfrage'
        verbose_name_plural = 'Sammelanlassanfragen'
