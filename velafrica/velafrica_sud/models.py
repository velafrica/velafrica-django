# -*- coding: utf-8 -*-
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords
from velafrica.organisation.models import Organisation
from velafrica.stock.models import StockList, Warehouse
from velafrica.core.ftp import MyFTPStorage
fs = MyFTPStorage()

class Country(models.Model):
    """
    Represents a country of the world.
    """
    name = models.CharField(blank=False, null=True, max_length=255, verbose_name="Name des Landes")
    flag = ResizedImageField(storage=fs, size=[500, 500], upload_to='velafrica_sud/country/flags/', blank=True, null=True, help_text='Flagge des Landes.')

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        ordering = ['-name']
        verbose_name_plural = "Countries"


class Forwarder(models.Model):
    """
    Represents a logistics partner.
    """
    name = models.CharField(blank=False, null=True, max_length=255, verbose_name="Name des Forwarders")

    history = HistoricalRecords()

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        ordering = ['name']


class Container(models.Model):
    """
    Represents a container.
    """
    organisation_from = models.ForeignKey(Organisation, blank=True, null=True, verbose_name='Verarbeitungspartner', help_text='Ort wo der Container geladen wurde.')
    warehouse_from = models.ForeignKey(Warehouse, blank=True, null=True, verbose_name='Export Lager', help_text='Lager wo die Velos verladen wurden')
    partner_to = models.ForeignKey('PartnerSud', blank=False, null=False, verbose_name='Destination')

    velos_loaded = models.IntegerField(blank=False, null=False, default=0, verbose_name='Anzahl Velos eingeladen')
    velos_unloaded = models.IntegerField(blank=False, null=False, default=0, verbose_name='Anzahl Velos ausgeladen')
    spare_parts = models.BooleanField(default=False, verbose_name='Ersatzteile transportiert?')
    stocklist = models.OneToOneField(StockList, null=True, blank=True)

    velos_worth = models.IntegerField(blank=False, null=False, default=0, verbose_name='Wert der Velos')   
    spare_parts_worth = models.IntegerField(blank=False, null=False, default=0, verbose_name='Wert der Ersatzteile')
    tools_worth = models.IntegerField(blank=False, null=False, default=0, verbose_name='Wert der Ersatzteile')
    various_worth = models.IntegerField(blank=False, null=False, default=0, verbose_name='Wert der Ersatzteile')
    
    pickup_date = models.DateField(blank=False, null=False, verbose_name='Ladedatum')
    shipment_date = models.DateField(blank=True, null=True, verbose_name='Verschiffungsdatum ab Europa') 
    arrival_port_date = models.DateField(blank=True, null=True, verbose_name='Ankunft Hafen Partner')
    arrival_partner_date = models.DateField(blank=True, null=True, verbose_name='Ankunft Partner')
    logistics = models.ForeignKey(Forwarder, blank=True, null=True, verbose_name='Forwarder', help_text='Logistikunternehmen')

    container_no = models.CharField(blank=True, null=True, max_length=255, verbose_name='Containernummer')
    seal_no = models.CharField(blank=True, null=True, max_length=255, verbose_name='Plombennummer')
    sgs_certified = models.BooleanField(default=False, verbose_name='SGS zertifiziert?')

    notes = models.TextField(blank=True, null=True, verbose_name="Bemerkungen zum Container")
    history = HistoricalRecords()

    def book(self):
        """
        Mark container as booked and add event to tracking.
        Returns (Success (bool), Amount of trackings edited (int))
        """

        from django.apps import apps

        Tracking = apps.get_model('sbbtracking', 'Tracking')
        TrackingEventType = apps.get_model('sbbtracking', 'TrackingEventType')

        trackings = Tracking.objects.filter(container=self)
        count = trackings.count()

        tet = TrackingEventType.objects.filter(arrival_africa=True).first()
        count_success = 0

        if not tet:
            print "No arrival_africa event type defined"
            return (False, count, 0)

        for t in trackings:
            if t.add_event(tet):
                count_success += 1

        return (True, count, count_success)

    def get_trimmed_container_no(self):
        if self.container_no:
            return self.container_no.replace(" ", "").replace("-", "")
        else:
            return None

    def __unicode__(self):
        return u"Container {} to {} ({})".format(self.container_no, self.partner_to, self.pickup_date)

    class Meta:
        ordering = ['-pickup_date']


class PartnerSud(models.Model):
    """
    Represents a partner of the Velafrica Sud Network.
    """
    name = models.CharField(blank=False, null=True, max_length=255, verbose_name="Name der Organisation")
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True, max_length=255, verbose_name="Website")
    image = ResizedImageField(storage=fs, size=[800, 800], upload_to='velafrica_sud/partner/', blank=True, null=True, help_text='Foto vom Partner vor Ort.')

    street = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name='Land')
    latitude = models.DecimalField(blank=True, null=True, verbose_name='Breitengrad', max_digits=9, decimal_places=6)
    longitude = models.DecimalField(blank=True, null=True, verbose_name='Längengrad', max_digits=9, decimal_places=6)

    org_type = models.CharField(max_length=255, blank=True, null=True)
    legalform = models.CharField(max_length=255, blank=True, null=True, verbose_name="Organisationsform")
    partner_since = models.IntegerField(blank=True, null=True, verbose_name="Partner seit...", help_text="Jahr")

    history = HistoricalRecords()

    def get_container_count(self):
        return Container.objects.filter(partner_to=self).count()
    get_container_count.short_description = 'Anzahl exp. Container'

    def get_bicycle_count(self):
        count = 0
        for c in Container.objects.filter(partner_to=self):
            count += c.velos_loaded
        return count
    get_bicycle_count.short_description = 'Anzahl exp. Velos'

    def __unicode__(self):
        return u"{}, {}".format(self.name, self.country)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Partner Süd"


class Report(models.Model):
    """
    """
    creation = models.DateField(default=timezone.now,)
    partner_sud = models.ForeignKey(PartnerSud)

    # employment opportunities -> Jahrangabe?
    employment_fulltime_men = models.IntegerField(verbose_name="Angestellte Vollzeit Männer")
    employment_fulltime_women = models.IntegerField(verbose_name="Angestellte Vollzeit Frauen")
    employment_parttime_men = models.IntegerField(verbose_name="Angestellte Teilzeit Männer")
    employment_parttime_women = models.IntegerField(verbose_name="Angestellte Teilzeit Frauen")
    employment_volunteer_men = models.IntegerField(verbose_name="Angestellte Freiwillige Männer")
    employment_volunteer_women = models.IntegerField(verbose_name="Angestellte Freiwillige Frauen")
    employment_internship_men = models.IntegerField(verbose_name="Angestellte Internship Männer")
    employment_internship_women = models.IntegerField(verbose_name="Angestellte Internship Frauen")
    employment_trainee_men = models.IntegerField(verbose_name="Angestellte Trainee Männer")
    employment_trainee_women = models.IntegerField(verbose_name="Angestellte Trainee Frauen")

    # economic data
    economic_bicycles_amount = models.IntegerField(verbose_name="Anzahl verkaufte Fahrräder")
    economic_bicycles_turnover = models.IntegerField(verbose_name="Umsatz Fahrräder")
    economic_spareparts_amount = models.IntegerField(verbose_name="Anzahl verkaufte Ersatzteile")
    economic_spareparts_turnover = models.IntegerField(verbose_name="Umsatz Ersatzteile")
    economic_services_amount = models.IntegerField(verbose_name="Anzahl verkaufte Dienstleistungen")
    economic_services_turnover = models.IntegerField(verbose_name="Umsatz Dienstleistungen")
    economic_turnover_total = models.IntegerField(verbose_name="Total Umsatz")

    economic_category1_name = models.CharField(verbose_name="Kategorie 1", max_length=255)
    economic_category1_pricerange = models.CharField(verbose_name="Preisrange Kategorie 1", max_length=255)
    economic_category2_name = models.CharField(verbose_name="Kategorie 2", max_length=255)
    economic_category2_pricerange = models.CharField(verbose_name="Preisrange Kategorie 2", max_length=255)
    economic_category3_name = models.CharField(verbose_name="Kategorie 3", max_length=255)
    economic_category3_pricerange = models.CharField(verbose_name="Preisrange Kategorie 3", max_length=255)
    economic_category4_name = models.CharField(verbose_name="Kategorie 4", max_length=255)
    economic_category4_pricerange = models.CharField(verbose_name="Preisrange Kategorie 4", max_length=255)
    economic_category5_name = models.CharField(verbose_name="Kategorie 5", max_length=255)
    economic_category5_pricerange = models.CharField(verbose_name="Preisrange Kategorie 5", max_length=255)
    economic_category6_name = models.CharField(verbose_name="Kategorie 6", max_length=255)
    economic_category6_pricerange = models.CharField(verbose_name="Preisrange Kategorie 6", max_length=255)
    economic_category7_name = models.CharField(verbose_name="Kategorie 7", max_length=255)
    economic_category7_pricerange = models.CharField(verbose_name="Preisrange Kategorie 7", max_length=255)
    economic_category8_name = models.CharField(verbose_name="Kategorie 8", max_length=255)
    economic_category8_pricerange = models.CharField(verbose_name="Preisrange Kategorie 8", max_length=255)

    PAYMENT_TYPE_CHOICES = (
        ('cash', 'Cash Payment'),
        ('installment', 'Installment'),
        ('card', 'Payment with Credit/Debit Card'),
        ('phone', 'Payment with Mobile Phone'),
        ('microloan', 'Micro Loan (e.g. in cooperation with Micro Finance Institution)'),
        ('other', 'Other'),
    )

    economic_payment_types = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)

    # vocational program and schooling

    DURATION_CHOICES = (
        ('0', 'less than 3 months'),
        ('1', '6 - 12 months'),
        ('2', '12 - 18 months'),
        ('3', '18 - 24 months'),
        ('4', 'more than 24 months'),
    )

    vocational_program_duration = models.CharField(max_length=1, choices=DURATION_CHOICES)
    vocational_program_girls = models.IntegerField(verbose_name="Anzahl Mädchen im Ausbildungsprogramm")
    vocational_program_boys = models.IntegerField(verbose_name="Anzahl Jungen im Ausbildungsprogramm")
    vocational_completed_girls = models.IntegerField(verbose_name="Anzahl Mädchen Ausbildungsprogramm abgeschlossen")
    vocational_completed_boys = models.IntegerField(verbose_name="Anzahl Jungen Ausbildungsprogramm abgeschlossen")
    vocational_exstudents_employed = models.IntegerField(verbose_name="Studenten vom letzten Jahr die jetzt angestellt sind")
    vocational_exstudents_selfemployed_new = models.IntegerField(verbose_name="Studenten vom letzten Jahr die jetzt bei einem anderen Betrieb angestellt sind")
    vocational_exstudents_selfemployed_link = models.IntegerField(verbose_name="Studenten vom letzten Jahr die jetzt bei einem Partnerbetrieb angestellt sind")

    # mobility program
    mobilityprogram = models.BooleanField(default=False)
    mobilityprogram_people_benefitted = models.IntegerField(verbose_name="Number of people that benefitted from mobility programm")
    mobilityprogram_financial_support = models.BooleanField(default=False, verbose_name="Mobilitätsprogramm finanziell von Velafrica unterstützt?")

    # community and social impact
    communityproject_reinvest_profit = models.BooleanField(default=False, verbose_name="Gewinn vom letzten Jahr in Community Projekte investiert?")
    
    COMMUNITY_AREA_TYPES_CHOICES = (
        ('0', 'Schooling / Education'),
        ('1', 'Entrepreneuership'),
        ('2', 'Evnironment / Environmental protection'),
        ('3', 'Mobility'),
        ('4', 'Women\'s empowerment'),
        ('5', 'Children\'s empowerment'),
        ('6', 'Sports activities'),
        ('7', 'Other'),
    )
    communityproject_areas = models.CharField(max_length=1, choices=COMMUNITY_AREA_TYPES_CHOICES, verbose_name="Feld der Gemeinschaftsarbeit")
    communityproject_reinvest_profit_total = models.IntegerField(verbose_name="In Gemeinschaftsprojekte re-investierter Betrag")
    communityproject_people_benefitted = models.CharField(max_length=255, verbose_name="Anzahl Personen die profitiert haben vom Gemeinschaftsprojekt")

    # Quality Assessment (values: 1 - 10)
    #quality_bicycles
    #quality_spares
    #quality_tools
    
    class Meta:
        ordering = ['-creation']
