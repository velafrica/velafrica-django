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
