# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
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
    organisation = models.ForeignKey(Organisation, blank=True, null=True, help_text='Organisation welcher das Fahrzeug gehört.', on_delete=models.CASCADE)
    image = ResizedImageField(size=[500, 500], upload_to='stock/categories/', blank=True, null=True, help_text='Foto des Fahrzeugs')
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
    organisation = models.ForeignKey(Organisation, blank=True, null=True, help_text='Organisation bei welcher der Fahrer angestellt ist.', on_delete=models.SET_NULL)
    active = models.BooleanField(default=True, help_text='Ist der Fahrer noch bei Velafrica? Inaktive Fahrer werden als (inaktiv) in der Auswahl bei den Fahrten aufgeführtgi.')

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

    :model:`stock.StockList`
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
        blank=True,    # TODO: change to false as soon as all rides are within the new format
        default="",
        verbose_name="Auftrag erstellt von"
    )
    velo_state = models.ForeignKey(
        VeloState,
        blank=True,
        null=True,
        verbose_name='Zustand der Velos',
        on_delete=models.CASCADE
    )
    planned_velos = models.CharField(max_length=255, blank=True, null=True, verbose_name='Anzahl')
    request_category = models.ForeignKey(
        RequestCategory,
        on_delete=models.CASCADE,
        verbose_name='Auftragsart',
        blank=True,
        null=True,
    )
    request_comment = models.CharField(
        max_length=255,
        verbose_name='Bemerkung',
        blank=True,
        default="",
        help_text="Bemerkung zum Auftrag"
    )

    # ride
    date = models.DateField(blank=True, null=True, default=timezone.now, verbose_name=u"Ausführdatum")
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
    velos = models.IntegerField(blank=True, null=True, default=0, verbose_name='Anzahl Velos')
    spare_parts = models.BooleanField(default=False, verbose_name='Ersatzteile transportiert?')
    stocklist = models.OneToOneField(StockList, null=True, blank=True, on_delete=models.SET_NULL)
    note = models.CharField(blank=True, null=True, max_length=255, verbose_name="Bemerkung",
                            help_text="Bemerkung zum Fahrt")
    completed = models.BooleanField(default=False, verbose_name="Auftrag ausgeführt")

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
    from_contact_phone = models.CharField(max_length=255, blank=True, default="", verbose_name="Telefonnummer")
    from_comment = models.CharField(max_length=255, blank=True, default="", verbose_name="Bemerkung",
                                    help_text="Bemerkung zum Abholort")

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
    to_comment = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Bemerkung",
        help_text="Bemerkung zur Lieferadresse"
    )

    # customer
    customer_company = models.CharField(max_length=255, blank=True, default="", verbose_name="Firma")
    customer_salutation = models.CharField(max_length=255, blank=True, default="", verbose_name="Anrede")
    customer_firstname = models.CharField(max_length=255, blank=True, default="", verbose_name="Vorname")
    customer_lastname = models.CharField(max_length=255, blank=True, default="", verbose_name="Nachname")
    customer_email = models.CharField(max_length=255, blank=True, default="", verbose_name="Email")
    customer_phone = models.CharField(max_length=255, blank=True, default="", verbose_name="Telefon")
    customer_street_nr = models.CharField(max_length=255, blank=True, default="", verbose_name="Strasse, Nr.")
    customer_zip_code = models.CharField(max_length=255, blank=True, default="", verbose_name="PLZ")
    customer_city = models.CharField(max_length=255, blank=True, default="", verbose_name="Ort")

    # invoice
    invoice_same_as_customer = models.BooleanField(default=True)
    charged = models.BooleanField(default=False, verbose_name="Kostenpflichtig")
    price = models.IntegerField(default=0, verbose_name="Preis")
    invoice_company_name = models.CharField(max_length=255, blank=True, default="", verbose_name="Firmenname")
    invoice_company_addition = models.CharField(max_length=255, blank=True, default="", verbose_name="Firmenzusatz")
    invoice_street_nr = models.CharField(max_length=255, blank=True, default="", verbose_name="Strasse, Nr.")
    invoice_zip_code = models.CharField(max_length=255, blank=True, default="", verbose_name="PLZ")
    invoice_city = models.CharField(max_length=255, blank=True, default="", verbose_name="Ort")
    invoice_commissioned = models.BooleanField(default=False, verbose_name="Rechnung in Auftrag gegeben")

    # optional ride data
    distance = models.IntegerField(verbose_name="Ungefähre Distanz in Meter", blank=True, null=True)

    history = HistoricalRecords()

    def get_distance(self):
        """
        Get distance from start to end of the driven way, using the Google Maps API.
        """
        loc1 = self.from_warehouse.get_geolocation()
        loc2 = self.to_warehouse.get_geolocation()
        if loc1 and loc2:
            result = utils.get_distance(loc1, loc2)
            if type(result) == int:
                self.distance = result
                self.save()
                return result
        return None

    def get_googlemaps_url(self):
        """
        """
        start = self.from_warehouse.get_address()
        end = self.to_warehouse.get_address()
        if start and end:
            if start.city and start.country and end.city and end.country:
                return utils.get_googlemaps_url_distance(self.from_warehouse.get_address(), self.to_warehouse.get_address())
        return None


    def __str__(self):
        try:
            return u"Fahrt {}, {}: {} nach {}".format(self.id, self.date, self.from_warehouse, self.to_warehouse)
        except:
            return u"Fahrt {}".format(self.id)

    class Meta:
        ordering = [
            'completed',
            '-date',
            '-date_created'
        ]
