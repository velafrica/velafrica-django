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


class SbbTicketOrder(models.Model):
    dropoff = models.ForeignKey('collection.Dropoff', on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=255, verbose_name="Vorname")
    last_name = models.CharField(max_length=255, verbose_name="Nachname")
    address = models.CharField(max_length=255, verbose_name="Strasse und Hausnummer")
    zip = models.CharField(max_length=255, verbose_name="PLZ und Ort")
    email = models.CharField(max_length=255, verbose_name="E-Mail")
    phone = models.CharField(max_length=255, verbose_name="Telefonnummer", blank=True)
    note = models.TextField(verbose_name="Bemerkung", blank=True)
    amount = models.IntegerField(verbose_name="Anzahl", default=1)

    def __unicode__(self):
        return u"{} {} - {}".format(self.first_name, self.last_name, self.dropoff)

    class Meta:
        verbose_name = 'SBB Ticketbestellung'
        verbose_name_plural = 'SBB Ticketbestellungen'


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
    organizer_type = models.IntegerField(verbose_name="Veranstalter", choices=PERSON_TYPE_CHOICES, default=1)

    collected_before = models.BooleanField(default=False, verbose_name="Bereits für Velafrica gesammelt")
    collected_before_note = models.TextField(blank=True, verbose_name="Wann und wo")

    # optional/detail information
    date_fixed = models.BooleanField(default=False, verbose_name='Datum fixiert')
    date = models.DateField(blank=True, null=True, verbose_name="Datum")
    pickup_time_start = models.CharField(max_length=255, verbose_name="Annahmezeit von", blank=True)
    pickup_time_end = models.CharField(max_length=255, verbose_name="Annahmezeit bis", blank=True)
    address = models.CharField(max_length=255, verbose_name='Adresse', blank=True)
    zip = models.CharField(max_length=255, verbose_name="Postleitzahl", blank=True)
    address_note = models.TextField(verbose_name="Standortbeschreibung", blank=True)
    expected_velos = models.IntegerField(verbose_name="Erwartete Menge gesammelter Velos", choices=EXPECTED_VELOS,
                                         default=1)
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


class ContactRequest(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='Vorname')
    last_name = models.CharField(max_length=255, verbose_name='Nachname')
    email = models.CharField(max_length=255, verbose_name='E-Mail')
    note = models.TextField(verbose_name='Nachricht')

    class Meta:
        verbose_name = 'Kontaktanfrage'
        verbose_name_plural = 'Kontaktanfragen'


class Content(models.Model):
    language = models.CharField(max_length=2, verbose_name='Sprache')
    path = models.CharField(max_length=255, verbose_name='Pfad')
    key = models.CharField(max_length=255, verbose_name='Key')
    value = models.TextField(verbose_name='Value', blank=True)
    description = models.TextField(verbose_name='Beschreibung', blank=True)

    def __unicode__(self):
        if self.path == 'index':
            return u"{}_{}_{}".format(self.language, self.path, self.key)
        else:
            return u"{}{}{}".format(self.language, self.path, self.key)

    class Meta:
        verbose_name = 'Inhalt'
        verbose_name_plural = 'Inhalte'


class TeamMember(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=255, verbose_name="Name")
    position = models.CharField(max_length=255, verbose_name="Position", blank=True)
    email = models.CharField(max_length=255, verbose_name="E-Mail", blank=True)
    image = models.CharField(max_length=255, verbose_name="Bild-URL", blank=True)
    sorting = models.IntegerField(verbose_name="Sortierung", default=0)

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        verbose_name = 'Teammitglied'
        verbose_name_plural = 'Teammitglieder'


class References(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=255, verbose_name="Name")
    image = models.CharField(max_length=255, verbose_name="Bild-URL")
    text = models.TextField(verbose_name="Text")
    sorting = models.IntegerField(verbose_name="Sortierung", default=0)

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        verbose_name = 'Botschafter'
        verbose_name_plural = 'Botschafter'


class Partner(models.Model):
    COUNTRY_CHOICES = (
        (1, 'Afrika'),
        (2, 'Schweiz'),
    )

    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(verbose_name="Beschreibung", blank=True)
    link = models.CharField(max_length=255, verbose_name="URL", blank=True)
    country = models.IntegerField(verbose_name="Land", choices=COUNTRY_CHOICES)
    location = models.CharField(max_length=255, verbose_name="Kanton/Staat")
    city = models.CharField(max_length=255, verbose_name="Stadt")

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partner'


class Event(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    category = models.ForeignKey('collection.EventCategory', related_name='pub_event_category', on_delete=models.SET_NULL, verbose_name="Kategorie", null=True)
    address = models.ForeignKey('organisation.Address', related_name='pub_event_address', on_delete=models.SET_NULL, verbose_name="Adresse", null=True)
    description = models.TextField(verbose_name="Beschreibung", blank=True)
    organizer = models.CharField(max_length=255, verbose_name="Veranstalter", blank=True)
    active = models.BooleanField(default=True, verbose_name="Aktiv")

    def get_date(self):
        all = self.datetimes.filter(event_id=self.id).order_by('-date')
        count = all.count()
        if count == 1:
            date = u"{}".format(all.first().date.strftime('%d.%m.%Y'))
        elif count > 1:
            date = u"{} - {}".format(all.first().date.strftime('%d.%m'), all.last().date.strftime('%d.%m.%Y'))
        else:
            date = ""
        return date

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        verbose_name = 'Veranstaltung'
        verbose_name_plural = 'Veranstaltungen'


class EventDateTime(models.Model):
    event = models.ForeignKey(Event, related_name="datetimes")
    date = models.DateField(verbose_name="Datum")
    time_start = models.CharField(max_length=255, verbose_name="Von", blank=True)
    time_end = models.CharField(max_length=255, verbose_name="Bis", blank=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'Datum/Uhrzeit'


class Supporter(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.CharField(max_length=140, verbose_name="Kurzbeschreibung", help_text="Max. 140 Zeichen", blank=True)
    link = models.URLField(verbose_name="URL")
    image = models.CharField(max_length=255, verbose_name="Bild/Logo URL", blank=True)
    sorting = models.IntegerField(verbose_name="Sortierung", default=0)
    active = models.BooleanField(verbose_name="Aktiv", default=True)

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        verbose_name = "Unterstützer"
        verbose_name_plural = "Unterstützer"
