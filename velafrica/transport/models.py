# -*- coding: utf-8 -*-
from django.db import models
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords

from velafrica.core import utils
from velafrica.organisation.models import Organisation
from velafrica.stock.models import Warehouse, StockList


class Car(models.Model):
    """
    Represents a car.
    """
    name = models.CharField(blank=False, null=True, max_length=255, verbose_name="Name des Fahrzeugs")
    organisation = models.ForeignKey(Organisation, blank=True, null=True,
                                     help_text='Organisation welcher das Fahrzeug gehört.', on_delete=models.CASCADE)
    image = ResizedImageField(size=[500, 500], upload_to='stock/categories/', blank=True, null=True,
                              help_text='Foto des Fahrzeugs')
    plate = models.CharField(blank=True, null=True, max_length=255, verbose_name='Autokennzeichen')

    history = HistoricalRecords()

    def __str__(self):
        return u"{}".format(self.name)

    class Meta:
        ordering = ['name']


class Driver(models.Model):
    """
    Represents a driver.
    """
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Name des Fahrers")
    organisation = models.ForeignKey(Organisation, blank=True, null=True,
                                     help_text='Organisation bei welcher der Fahrer angestellt ist.',
                                     on_delete=models.SET_NULL)
    active = models.BooleanField(default=True,
                                 help_text='Ist der Fahrer noch bei Velafrica? '
                                           'Inaktive Fahrer werden als (inaktiv) '
                                           'in der Auswahl bei den Fahrten aufgeführt.')

    history = HistoricalRecords()

    def __str__(self):
        if not self.active:
            return u"{} (inaktiv)".format(self.name)
        return u"{}".format(self.name)

    class Meta:
        ordering = ['-active', 'name']


class VeloState(models.Model):
    """
    Represents the state of a bicycle.
    """
    name = models.CharField(blank=False, null=False, max_length=40, verbose_name="Name des Zustandes")
    description = models.CharField(blank=True, null=True, max_length=255, verbose_name="Beschreibung")

    history = HistoricalRecords()

    def __str__(self):
        return u"{}".format(self.name)

    class Meta:
        ordering = ['name']


class RequestCategory(models.Model):
    category_name = models.CharField(max_length=255, blank=True, default="", verbose_name="Name")

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "request categories"


class Ride(models.Model):
    """
    Represents a ride from one destination to the other.
    Used to count how many bicycles went from one place to another in a certain period of time.
    """

    # request
    date_created = models.DateField(
        auto_now_add=True,
        null=True,
        verbose_name="Auftrag erstellt am",
    )
    date_modified = models.DateField(
        auto_now=True,
        null=True,
        verbose_name="Bearbeitet am"
    )
    created_by = models.CharField(
        max_length=255,
        blank=False,
        default="",
        verbose_name="Auftrag erstellt von (Vor- und Nachname)"
    )
    velo_state = models.ForeignKey(
        VeloState,
        blank=True,
        null=True,
        verbose_name='Transportgut',
        on_delete=models.CASCADE
    )
    planned_velos = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Anzahl Velos (voraussichtlich)',
    )
    request_category = models.ForeignKey(
        RequestCategory,
        on_delete=models.CASCADE,
        verbose_name='Kategorie Velospender',
        blank=True,
        null=True,
    )
    request_comment = models.TextField(
        verbose_name='Bemerkung',
        blank=True,
        default="",
        help_text="Bemerkung zum Auftrag"
    )

    # ride
    date = models.DateField(blank=True, null=True, verbose_name=u"Vereinbarter Abholtermin")
    pickup_time = models.CharField(blank=True, default="", max_length=30, verbose_name="Vereinbarte Abholzeit")
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        verbose_name='Fahrer',
        blank=True,
        null=True,
        help_text='Person die den Transport durchgeführt hat.'
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        verbose_name='Fahrzeug',
        blank=True,
        null=True
    )
    velos = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='Anzahl transportierter Velos',
        help_text='Wird durch den Transport ausgefüllt.'
    )
    spare_parts = models.BooleanField(default=False, verbose_name='Ersatzteile transportiert?')
    stocklist = models.OneToOneField(StockList, null=True, blank=True, on_delete=models.SET_NULL)
    note = models.TextField(blank=True, null=True, verbose_name="Bemerkung",
                            help_text="Bemerkung zum Fahrt")
    completed = models.BooleanField(default=False, verbose_name="Auftrag ausgeführt")
    printed = models.BooleanField(default=False, verbose_name="Auftrag gedruckt")

    # from
    from_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='from_warehouse',
        verbose_name='Start',
        blank=True,
        null=True,
        help_text='Start der Fahrt',
    )
    from_street_nr = models.CharField(max_length=255, blank=True, default="", verbose_name="Strasse, Nr.")
    from_zip_code = models.CharField(max_length=255, blank=True, default="", verbose_name="PLZ")
    from_city = models.CharField(max_length=255, blank=True, default="", verbose_name="Ort")
    from_contact_name = models.CharField(max_length=255, blank=True, default="", verbose_name="Kontaktperson")
    from_contact_phone = models.CharField(max_length=255, blank=True, default="", verbose_name="Tel. Nr. (Mobile)")
    from_comment = models.TextField(
        blank=True,
        default="",
        verbose_name="Details Standort",
        help_text="Details zum Abholstandort"
    )

    # to
    to_warehouse = models.ForeignKey(
        Warehouse,
        verbose_name='Ziel',
        related_name='to_warehouse',
        help_text='Ziel der Fahrt',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    to_street_nr = models.CharField(max_length=255, blank=True, default="", verbose_name="Strasse, Nr.")
    to_zip_code = models.CharField(max_length=255, blank=True, default="", verbose_name="PLZ")
    to_city = models.CharField(max_length=255, blank=True, default="", verbose_name="Ort")
    to_contact_name = models.CharField(max_length=255, blank=True, default="", verbose_name="Kontaktperson")
    to_contact_phone = models.CharField(max_length=255, blank=True, default="", verbose_name="Tel. Nr. (Mobile)")
    to_comment = models.TextField(
        max_length=1024,
        blank=True,
        default="",
        verbose_name="Details Standort",
        help_text="Details zur Lieferadresse"
    )

    # customer
    customer_company = models.CharField(max_length=255, blank=True, default="", verbose_name="Firma")
    customer_salutation = models.CharField(max_length=255, blank=True, default="", verbose_name="Anrede")
    customer_firstname = models.CharField(max_length=255, blank=True, default="", verbose_name="Vorname")
    customer_lastname = models.CharField(max_length=255, blank=True, default="", verbose_name="Nachname")
    customer_email = models.CharField(max_length=255, blank=True, default="", verbose_name="Email")
    customer_phone = models.CharField(max_length=255, blank=True, default="", verbose_name="Tel. Nr.")
    customer_street_nr = models.CharField(max_length=255, blank=True, default="", verbose_name="Strasse, Nr.")
    customer_zip_code = models.CharField(max_length=255, blank=True, default="", verbose_name="PLZ")
    customer_city = models.CharField(max_length=255, blank=True, default="", verbose_name="Ort")

    # invoice
    invoice_same_as_customer = models.BooleanField(
        default=True,
        verbose_name="Rechnungsadresse = Kundenadresse",
        help_text="Standardmässig wird als Rechnungsempfänger die Adresse des Kunden (Auftraggeber) verwendet."
    )
    charged = models.BooleanField(default=False, verbose_name="Kostenpflichtig?")
    invoice_purpose = models.CharField(max_length=255, null=True, blank=True, verbose_name="Zweck")
    price = models.IntegerField(null=True, blank=True, verbose_name="Betrag exkl. MWSt.")
    cost_type = models.CharField(max_length=255, default="3510-506", blank=True,
                                 verbose_name="Kostenart und Kostenstelle")
    invoice_company_name = models.CharField(max_length=255, blank=True, default="", verbose_name="Firmenname")
    invoice_company_addition = models.CharField(max_length=255, blank=True, default="", verbose_name="Firmenzusatz")
    invoice_street_nr = models.CharField(max_length=255, blank=True, default="", verbose_name="Strasse, Nr.")
    invoice_zip_code = models.CharField(max_length=255, blank=True, default="", verbose_name="PLZ")
    invoice_city = models.CharField(max_length=255, blank=True, default="", verbose_name="Ort")
    invoice_commissioned = models.BooleanField(
        default=False,
        verbose_name="Rechnung der Buchhaltung in Auftrag gegeben",
        help_text="Wird nur durch die zuständige Person von Velafrica ausgefüllt",
    )

    # optional ride data
    distance = models.IntegerField(verbose_name="Ungefähre Distanz in Meter", blank=True, null=True)

    history = HistoricalRecords()

    # allow celery exports
    @classmethod
    def export_resource_classes(cls):
        from velafrica.transport.resources import RideResource
        return {
            'all rides': ('Ride resources', RideResource),
        }

    # admin helper methods
    def auftraggeber_str(self):
        str = ""
        if self.customer_company:
            str += self.customer_company
        if self.customer_firstname or self.customer_lastname:
            if len(str) > 0:
                str += ", "
            str += self.customer_firstname + " " + self.customer_lastname
        return str

    auftraggeber_str.short_description = 'Auftraggeber'

    def pickup_date(self):
        return self.date

    pickup_date.short_description = "Abholdatum"

    def pickup_date_time(self):
        return self.pickup_time

    pickup_date_time.short_description = "Zeit"

    def created_time(self):
        return self.date_created

    created_time.short_description = "Erstellt"

    def number_of_velos(self):
        return self.velos

    number_of_velos.short_description = "Velos"

    def get_status_ride(self):
        if self.completed:  # transport completed
            return "completed"
        elif self.date:  # date fix for transport
            return "fixed"
        elif self.printed:  # date fix for transport
            return "printed"
        else:  # nothing done yet
            return "new"

    def get_status_invoice(self):
        if not self.charged:
            return
        if self.invoice_commissioned:  # invoice sent
            return "success"
        return "danger"

    def get_distance(self):
        """
        Get distance from start to end of the driven way, using the Google Maps API.
        """
        if self.distance:
            return self.distance

        result = utils.get_distance(
            origin=utils.get_geolocation(self.get_from_address()),
            destination=utils.get_geolocation(self.get_to_address())
        )
        if type(result) == int:
            self.distance = result
            self.save()
            return result
        return None

    def get_googlemaps_url(self):
        start, end = self.get_from_address(), self.get_to_address()
        return utils.get_googlemaps_url_distance(start, end) if start and end else None

    def get_from_address(self):
        if self.from_warehouse and self.from_warehouse.get_address():
            return str(self.from_warehouse.get_address())
        address = ""
        if self.from_street_nr:
            address += u"{}".format(self.from_street_nr)
        if self.from_zip_code:
            address += u", {}".format(self.from_zip_code)
            if self.from_city:
                address += u" {}".format(self.from_city)
        elif self.from_city:
            address += u", {}".format(self.from_city)
        return address

    def get_to_address(self):
        if self.to_warehouse and self.to_warehouse.get_address():
            return str(self.to_warehouse.get_address())
        address = ""
        if self.to_street_nr:
            address += u"{}".format(self.to_street_nr)
        if self.to_zip_code:
            address += u", {}".format(self.to_zip_code)
            if self.to_city:
                address += u" {}".format(self.to_city)
        elif self.to_city:
            address += u", {}".format(self.to_city)
        return address

    def prepare_for_print(self):
        self.printed = True
        self.save()

        if self.from_warehouse and self.from_warehouse.get_address():
            self.from_street_nr = self.from_warehouse.get_address().street
            self.from_zip_code = self.from_warehouse.get_address().zipcode
            self.from_city = self.from_warehouse.get_address().city
            self.from_contact_name = self.from_warehouse.organisation.contact_person
            self.from_contact_phone = self.from_warehouse.organisation.phone

        if self.to_warehouse and self.to_warehouse.get_address():
            self.to_street_nr = self.to_warehouse.get_address().street
            self.to_zip_code = self.to_warehouse.get_address().zipcode
            self.to_city = self.to_warehouse.get_address().city
            self.to_contact_name = self.to_warehouse.organisation.contact_person
            self.to_contact_phone = self.to_warehouse.organisation.phone
        return self

    def __str__(self):
        return u"Transport {}".format(self.id)

    def save(self, *args, **kwargs):
        # copy customer info for invoice
        if self.charged and self.invoice_same_as_customer:
            if not self.invoice_company_name:
                self.invoice_company_name = self.customer_company
            if not self.invoice_street_nr:
                self.invoice_street_nr = self.customer_street_nr
            if not self.invoice_zip_code:
                self.invoice_zip_code = self.customer_zip_code
            if not self.invoice_city:
                self.invoice_city = self.customer_city

        super().save(*args, **kwargs)

    class Meta:
        ordering = [
            'completed',
            '-date',
            '-date_created'
        ]
