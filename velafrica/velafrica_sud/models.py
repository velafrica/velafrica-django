# -*- coding: utf-8 -*-
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField
from multiselectfield import MultiSelectField
from simple_history.models import HistoricalRecords
from velafrica.organisation.models import Organisation, Address
from velafrica.stock.models import StockList, Warehouse
from velafrica.core.ftp import MyFTPStorage
fs = MyFTPStorage()


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

    velos_worth = models.IntegerField(blank=False, null=False, default=0, verbose_name='Wert Velos')   
    spare_parts_worth = models.IntegerField(blank=False, null=False, default=0, verbose_name='Wert Ersatzteile')
    tools_worth = models.IntegerField(blank=False, null=False, default=0, verbose_name='Wert Werkzeuge')
    various_worth = models.IntegerField(blank=False, null=False, default=0, verbose_name='Wert Anderes')
    
    pickup_date = models.DateField(blank=False, null=False, verbose_name='Ladedatum')
    shipment_date = models.DateField(blank=True, null=True, verbose_name='Verschiffungsdatum ab Europa') 
    arrival_port_date = models.DateField(blank=True, null=True, verbose_name='Ankunft Hafen Partner')
    arrival_partner_date = models.DateField(blank=True, null=True, verbose_name='Ankunft Partner')
    logistics = models.ForeignKey(Forwarder, blank=True, null=True, verbose_name='Forwarder', help_text='Logistikunternehmen')

    container_no = models.CharField(blank=True, null=True, max_length=255, verbose_name='Containernummer')
    seal_no = models.CharField(blank=True, null=True, max_length=255, verbose_name='Plombennummer')
    sgs_certified = models.BooleanField(default=False, verbose_name='SGS zertifiziert?')

    notes = models.TextField(blank=True, null=True, verbose_name="Bemerkungen zum Container")

    booked = models.BooleanField(default=False, verbose_name="Abgeschlossen")

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

        self.booked = True
        self.save()

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

    def container_n_of_all(self):
        """
        Returns number of how many containers have been shipped up to this one.
        """

        ct = self
        # get oldest container by pickup date
        first = Container.objects.all().last()
        pos = Container.objects.filter(pickup_date__range=[first.pickup_date, ct.pickup_date]).count()
        return pos
    container_n_of_all.verbose_name = "Container Nummer"
    container_n_of_all.short_description = "#"

    def container_n_of_partner(self):
        """
        Returns number of how many containers have been shipped to this partner up to this one.
        """
        ct = self
        # get oldest container by pickup date
        first = Container.objects.all().last()
        pos = Container.objects.filter(partner_to=self.partner_to).filter(pickup_date__range=[first.pickup_date, ct.pickup_date]).count()
        return pos
    container_n_of_all.verbose_name = "Container Nummer Partner"
    container_n_of_all.short_description = "#"

    def container_n_of_year(self):
        """
        Returns number of how many containers have been shipped this year up to this one.
        """
        ct = self
        # get oldest container by pickup date
        first = Container.objects.all().filter(pickup_date__range=[timezone.datetime(ct.pickup_date.year,1,1), ct.pickup_date]).last()
        pos = Container.objects.filter(partner_to=self.partner_to).filter(pickup_date__range=[first.pickup_date, ct.pickup_date]).count()
        return pos
    container_n_of_year.verbose_name = "Container dieses Jahr"
    container_n_of_year.short_description = "# / Jahr"

    def __unicode__(self):
        if self.container_no:
            return u"{} - {} ({})".format(self.container_no, self.partner_to, self.pickup_date)
        else:
            return u"{} ({})".format(self.partner_to, self.pickup_date)

    class Meta:
        ordering = ['-pickup_date']


class PartnerSud(models.Model):
    """
    Represents a partner of the Velafrica Sud Network.
    """
    organisation = models.OneToOneField(Organisation, blank=False, null=False, related_name="partnersud")
    image = ResizedImageField(storage=fs, size=[800, 800], upload_to='velafrica_sud/partner/', blank=True, null=True, help_text='Foto vom Partner vor Ort.')

    # partner sud info
    org_type = models.CharField(max_length=255, blank=True, null=True)
    legalform = models.CharField(max_length=255, blank=True, null=True, verbose_name="Organisationsform")
    partner_since = models.IntegerField(blank=True, null=True, verbose_name="Partner seit...", help_text="Jahr")
    vocational_training = models.BooleanField(default=False, verbose_name="Bietet Berufsbildung an")
    infrastructure = models.TextField(verbose_name="Infrastruktur", help_text="Übersicht über die Infrastruktur vor Ort (Anzahl Arbeitsplätze, Lagermöglichkeiten, Art der Gebäude etc)", blank=True, null=True)

    history = HistoricalRecords()

    def get_name(self):
        """
        """
        return self.organisation.name
    get_name.short_description = "Name"

    def get_address(self):
        """
        """
        return self.organisation.address
    get_address.short_description = "Adresse"

    def get_website(self):
        """
        """
        return self.organisation.website
    get_website.short_description = "Website"

    def get_facebook(self):
        """
        """
        return self.organisation.facebook
    get_facebook.short_description = "Facebook"

    def get_contact(self):
        """
        """
        return self.organisation.contact
    get_contact.short_description = "Kontaktperson"

    def get_description(self):
        """
        """
        return self.organisation.description
    get_description.short_description = "Description"

    def get_country(self):
        """
        """
        if self.organisation.address:
            return self.organisation.address.country
        else:
            return None
    get_country.short_description = "Land"

    def get_container_count(self):
        """
        Get number of containers that have been shipped to this partner.
        """
        return Container.objects.filter(partner_to=self).count()
    get_container_count.short_description = 'Anzahl exp. Container'

    def get_bicycle_count(self):
        """
        Get number of bicycles that have been shipped to this partner.
        """
        count = 0
        for c in Container.objects.filter(partner_to=self):
            count += c.velos_loaded
        return count
    get_bicycle_count.short_description = 'Anzahl exp. Velos'

    def __unicode__(self):
        return u"{}, {}".format(self.organisation.name, self.organisation.address.country)

    class Meta:
        ordering = ['organisation__name']
        verbose_name_plural = "Partner Süd"


class Role(models.Model):
    """
    Name of a role of PartnerSud staff.
    """
    name = models.CharField(verbose_name="Name", max_length=255, unique=True)

    def __unicode__(self):
        return self.name

class Staff(models.Model):
    """
    Used to add information about personal staff at partner.
    """
    role = models.ForeignKey(Role,verbose_name="Rolle")
    salary = models.IntegerField(verbose_name="Salär (USD)")
    number = models.IntegerField(verbose_name="Anzahl Angestellte")
    report = models.ForeignKey('Report', verbose_name="Report")
    history = HistoricalRecords()

    def __unicode__(self):
        return u"{} {}s earning a total of {} USD".format(self.number, self.role, self.salary)


class Report(models.Model):
    """
    Reports are used to gather feedback and detailed information about a partner.

    TODO: currency to USD functions & add these to Resource
    """
    creation = models.DateField(default=timezone.now,)
    partner_sud = models.ForeignKey(PartnerSud)
    currency = models.CharField(blank=False, null=True, default="", max_length=10, verbose_name="Verwendete Währung bei Finanzangaben")
    currency_rate = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=10, default=1.0, verbose_name="Währungskurs zu USD")

    # employment opportunities -> Jahrangabe?
    employment_fulltime_men = models.IntegerField(verbose_name="Angestellte Vollzeit Männer",blank=True, null=True)
    employment_fulltime_women = models.IntegerField(verbose_name="Angestellte Vollzeit Frauen",blank=True, null=True)
    employment_parttime_men = models.IntegerField(verbose_name="Angestellte Teilzeit Männer",blank=True, null=True)
    employment_parttime_women = models.IntegerField(verbose_name="Angestellte Teilzeit Frauen",blank=True, null=True)
    employment_volunteer_men = models.IntegerField(verbose_name="Angestellte Freiwillige Männer",blank=True, null=True)
    employment_volunteer_women = models.IntegerField(verbose_name="Angestellte Freiwillige Frauen",blank=True, null=True)
    employment_internship_men = models.IntegerField(verbose_name="Angestellte Internship Männer",blank=True, null=True)
    employment_internship_women = models.IntegerField(verbose_name="Angestellte Internship Frauen",blank=True, null=True)
    employment_trainee_men = models.IntegerField(verbose_name="Angestellte Trainee Männer",blank=True, null=True)
    employment_trainee_women = models.IntegerField(verbose_name="Angestellte Trainee Frauen",blank=True, null=True)
    employment_notes = models.TextField(verbose_name="Jobs Beschreibung",blank=True, null=True)
    employment_salary_calculation = models.TextField(verbose_name="Berechnung der Saläre", help_text="Wie werden die Saläre / Kompensationen berechnet?", blank=True, null=True)

    # marketing
    CUSTOMER_SEGMENT_CHOICES = (
        ('men', 'Men'),
        ('women', 'Women'),
        ('children_students', 'Children/Students'),
        ('teachers', 'Teachers'),
        ('businessmen', 'Business Men'),
        ('retail', 'Bicycle Retail Agents'),
        ('wholesale', 'Bicycle Wholesale Agents'),
        ('farmers', 'Farmers'),
        ('safari', 'Safari companies'),
        ('hospitals', 'Hospitals'),
        ('other', 'other'),
    )
    marketing_customer_segments = MultiSelectField(max_length=255, choices=CUSTOMER_SEGMENT_CHOICES, blank=True, null=True, verbose_name="Kundensegmente")
    marketing_customer_segments_other = models.CharField(max_length=255, blank=True, null=True, verbose_name="Andere", help_text="Bitte ausfüllen, wenn bei der vorherigen Frage 'others' ausgewählt wurde.")
    marketing_customer_segments_top1 = models.CharField(choices=CUSTOMER_SEGMENT_CHOICES, max_length=255, verbose_name="Kundensegmente Top 1", blank=True, null=True)
    marketing_customer_segments_top2 = models.CharField(choices=CUSTOMER_SEGMENT_CHOICES, max_length=255, verbose_name="Kundensegmente Top 2", blank=True, null=True)
    marketing_customer_segments_top3 = models.CharField(choices=CUSTOMER_SEGMENT_CHOICES, max_length=255, verbose_name="Kundensegmente Top 3", blank=True, null=True)

    CHANNEL_CHOICES = (
        ('not_using_it', 'We don\'t use it'),
        ('rarely', 'rarely'),
        ('occasionally', 'occasionally'),
        ('often', 'often'),
        ('very often', 'very often'),
    )

    SELLING_CHANNEL_CHOICES = (
        ('not_good', 'not good'),
        ('ok', 'ok'),
        ('successful', 'successful'),
        ('not_using_it_yet', 'we do not use it (yet)'),
    )

    marketing_channels_mouth = models.CharField(max_length=1, choices=CHANNEL_CHOICES, blank=True, null=True)
    marketing_channels_radio = models.CharField(max_length=1, choices=CHANNEL_CHOICES, blank=True, null=True)
    marketing_channels_tv = models.CharField(max_length=1, choices=CHANNEL_CHOICES, blank=True, null=True)
    marketing_channels_socialmedia = models.CharField(max_length=1, choices=CHANNEL_CHOICES, blank=True, null=True)
    marketing_channels_poster = models.CharField(max_length=1, choices=CHANNEL_CHOICES, blank=True, null=True)
    marketing_channels_flyer = models.CharField(max_length=1, choices=CHANNEL_CHOICES, blank=True, null=True)
    marketing_channels_event_organisation = models.CharField(max_length=1, choices=CHANNEL_CHOICES, blank=True, null=True)
    marketing_channels_event_attendance = models.CharField(max_length=1, choices=CHANNEL_CHOICES, blank=True, null=True)
    marketing_channels_other = models.CharField(max_length=1, choices=CHANNEL_CHOICES, blank=True, null=True)

    marketing_sales_shop = models.CharField(verbose_name="Shop", max_length=1, choices=SELLING_CHANNEL_CHOICES, blank=True, null=True)
    marketing_sales_outlets = models.CharField(verbose_name="Outlet", max_length=1, choices=SELLING_CHANNEL_CHOICES, blank=True, null=True)
    marketing_sales_retail = models.CharField(verbose_name="Retail", max_length=1, choices=SELLING_CHANNEL_CHOICES, blank=True, null=True)
    marketing_sales_wholesale = models.CharField(verbose_name="Wholesale", max_length=1, choices=SELLING_CHANNEL_CHOICES, blank=True, null=True)
    marketing_sales_other = models.CharField(verbose_name="Andere", max_length=1, choices=SELLING_CHANNEL_CHOICES, blank=True, null=True)

    # economic data
    economic_bicycles_amount = models.IntegerField(verbose_name="Anzahl verkaufte Fahrräder",blank=True, null=True)
    economic_bicycles_turnover = models.IntegerField(verbose_name="Umsatz Fahrräder",blank=True, null=True)
    economic_spareparts_amount = models.IntegerField(verbose_name="Anzahl verkaufte Ersatzteile",blank=True, null=True)
    economic_spareparts_turnover = models.IntegerField(verbose_name="Umsatz Ersatzteile",blank=True, null=True)
    economic_services_amount = models.IntegerField(verbose_name="Anzahl verkaufte Dienstleistungen",blank=True, null=True)
    economic_services_turnover = models.IntegerField(verbose_name="Umsatz Dienstleistungen",blank=True, null=True)
    economic_turnover_total = models.IntegerField(verbose_name="Total Umsatz",blank=True, null=True)

    economic_import_taxes = models.CharField(verbose_name="Aktuelle Importzölle für gebrauchte Fahrräder", blank=True,null=True, max_length=255)
    economic_transport_costs_port_to_organisation = models.IntegerField(verbose_name="Aktuelle Kosten für Transport von Eingangshafen zur Organisation", blank=True, null=True)

    economic_category1_name = models.CharField(verbose_name="Kategorie 1", max_length=255,blank=True, null=True)
    economic_category1_pricerange = models.CharField(verbose_name="Preisrange Kategorie 1", max_length=255,blank=True, null=True)
    economic_category2_name = models.CharField(verbose_name="Kategorie 2", max_length=255,blank=True, null=True)
    economic_category2_pricerange = models.CharField(verbose_name="Preisrange Kategorie 2", max_length=255,blank=True, null=True)
    economic_category3_name = models.CharField(verbose_name="Kategorie 3", max_length=255,blank=True, null=True)
    economic_category3_pricerange = models.CharField(verbose_name="Preisrange Kategorie 3", max_length=255,blank=True, null=True)
    economic_category4_name = models.CharField(verbose_name="Kategorie 4", max_length=255,blank=True, null=True)
    economic_category4_pricerange = models.CharField(verbose_name="Preisrange Kategorie 4", max_length=255,blank=True, null=True)
    economic_category5_name = models.CharField(verbose_name="Kategorie 5", max_length=255,blank=True, null=True)
    economic_category5_pricerange = models.CharField(verbose_name="Preisrange Kategorie 5", max_length=255,blank=True, null=True)
    economic_category6_name = models.CharField(verbose_name="Kategorie 6", max_length=255,blank=True, null=True)
    economic_category6_pricerange = models.CharField(verbose_name="Preisrange Kategorie 6", max_length=255,blank=True, null=True)
    economic_category7_name = models.CharField(verbose_name="Kategorie 7", max_length=255,blank=True, null=True)
    economic_category7_pricerange = models.CharField(verbose_name="Preisrange Kategorie 7", max_length=255,blank=True, null=True)
    economic_category8_name = models.CharField(verbose_name="Kategorie 8", max_length=255,blank=True, null=True)
    economic_category8_pricerange = models.CharField(verbose_name="Preisrange Kategorie 8", max_length=255,blank=True, null=True)

    PAYMENT_TYPE_CHOICES = (
        ('cash', 'Cash Payment'),
        ('installment', 'Installment'),
        ('card', 'Payment with Credit/Debit Card'),
        ('phone', 'Payment with Mobile Phone'),
        ('microloan', 'Micro Loan (e.g. in cooperation with Micro Finance Institution)'),
        ('other', 'Other'),
    )

    economic_payment_types = MultiSelectField(max_length=20, choices=PAYMENT_TYPE_CHOICES, blank=True, null=True)
    economic_notes = models.TextField(verbose_name="Bemerkungen",blank=True, null=True)

    # vocational program and schooling

    DURATION_CHOICES = (
        ('less_than_3_months', 'less than 3 months'),
        ('6_to_12_months', '6 - 12 months'),
        ('12_to_18_months', '12 - 18 months'),
        ('18_to_24_months', '18 - 24 months'),
        ('more_than_24_months', 'more than 24 months'),
    )

    vocational_program_duration = models.CharField(verbose_name="Dauer des Beschäftigungsprogramms", max_length=1, choices=DURATION_CHOICES,blank=True, null=True)
    vocational_program_girls = models.IntegerField(verbose_name="Anzahl Mädchen im Ausbildungsprogramm",blank=True, null=True)
    vocational_program_boys = models.IntegerField(verbose_name="Anzahl Jungen im Ausbildungsprogramm",blank=True, null=True)
    vocational_completed_girls = models.IntegerField(verbose_name="Anzahl Mädchen Ausbildungsprogramm abgeschlossen",blank=True, null=True)
    vocational_completed_boys = models.IntegerField(verbose_name="Anzahl Jungen Ausbildungsprogramm abgeschlossen",blank=True, null=True)
    vocational_certificates = models.IntegerField(verbose_name="Ausgestellte Zertifikate dieses Jahr", blank=True, null=True)
    vocational_certificates_ack = models.IntegerField(verbose_name="Davon staatlich anerkannte Zertifikate", blank=True, null=True)
    vocational_exstudents_employed = models.IntegerField(verbose_name="Studenten vom letzten Jahr die jetzt angestellt sind",blank=True, null=True)
    vocational_exstudents_selfemployed_new = models.IntegerField(verbose_name="Studenten vom letzten Jahr die jetzt bei einem anderen Betrieb angestellt sind",blank=True, null=True)
    vocational_exstudents_selfemployed_link = models.IntegerField(verbose_name="Studenten vom letzten Jahr die jetzt bei einem Partnerbetrieb angestellt sind",blank=True, null=True)
    vocational_notes = models.TextField(verbose_name="Bemerkungen",blank=True, null=True)
    

    vocational_exstudents_bicycle_industry = models.IntegerField(verbose_name="Anzahl Ex-Studenten die jetzt im Velogewerbe arbeiten",blank=True, null=True)
    vocational_exstudents_agriculture = models.IntegerField(verbose_name="Anzahl Ex-Studenten die jetzt in der Landwirtschaft arbeiten",blank=True, null=True)
    vocational_exstudents_familiybusiness = models.IntegerField(verbose_name="Anzahl Ex-Studenten die jetzt im Familienbetrieb arbeiten",blank=True, null=True)
    vocational_exstudents_energy = models.IntegerField(verbose_name="Anzahl Ex-Studenten die jetzt im Energie Sektor arbeiten",blank=True, null=True)

    # mobility program
    mobilityprogram = models.BooleanField(default=False)
    mobilityprogram_people_benefitted = models.CharField(max_length=255, verbose_name="Anzahl Personen die vom Mobilitätsprogramm profitiert haben",blank=True, null=True)
    mobilityprogram_financial_support = models.BooleanField(default=False, verbose_name="Mobilitätsprogramm finanziell von Velafrica unterstützt?")
    mobilityprogram_notes = models.TextField(verbose_name="Bemerkungen",blank=True, null=True)

    # community and social impact
    communityproject_reinvest_profit = models.BooleanField(default=False, verbose_name="Gewinn vom letzten Jahr in Community Projekte investiert?")
    
    COMMUNITY_AREA_TYPES_CHOICES = (
        ('education', 'Schooling / Education'),
        ('entrepreneurship', 'Entrepreneuership'),
        ('environment', 'Evnironment / Environmental protection'),
        ('mobility', 'Mobility'),
        ('women_empowerment', 'Women\'s empowerment'),
        ('children_empowerment', 'Children\'s empowerment'),
        ('sports_activist', 'Sports activities'),
        ('other', 'Other'),
    )
    communityproject_areas = models.CharField(max_length=1, choices=COMMUNITY_AREA_TYPES_CHOICES, verbose_name="Feld der Community Arbeit",blank=True, null=True)
    communityproject_reinvest_profit_total = models.IntegerField(verbose_name="In Community Projekt re-investierter Betrag",blank=True, null=True)
    communityproject_people_benefitted = models.CharField(max_length=255, verbose_name="Anzahl Personen die vom Community Projekt profitiert haben",blank=True, null=True)
    communityproject_manager = models.BooleanField(default=False, verbose_name="Community Manager vorhanden?")
    communityproject_notes = models.TextField(verbose_name="Bemerkungen",blank=True, null=True)

    # Quality Assessment (values: 1 - 10)
    QUALITY_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )
    cooperation_quality_bicycles = models.CharField(verbose_name="Qualität der gelieferten Velos", max_length=2, choices=QUALITY_CHOICES, blank=True, null=True)
    cooperation_quality_spares = models.CharField(verbose_name="Qualität der gelieferten Ersatzteile", max_length=2, choices=QUALITY_CHOICES, blank=True, null=True)
    cooperation_quality_tools = models.CharField(verbose_name="Qualität der gelieferten Werkzeuge", max_length=2, choices=QUALITY_CHOICES, blank=True, null=True)
    cooperation_ordering_experience = models.TextField(verbose_name="Bestellerlebnis", help_text="Wie wird das Bestellen der Fahrräder und Ersatzteile empfunden?", blank=True, null=True)
    cooperation_comments = models.TextField(verbose_name="Allgemeine Kommentare zur Partnerschaft", blank=True, null=True)

    # final comments
    final_biggest_success = models.TextField(blank=True, null=True, verbose_name="Grösste Erfolge dieses Jahres?")
    final_future_challenges = models.TextField(blank=True, null=True, verbose_name="Grösste Herausforderungen der Zukunft?")

    history = HistoricalRecords()

    class Meta:
        ordering = ['-creation']

    # TODO: add to admin
    def economic_bicycles_turnover_USD(self):
        if self.economic_bicycles_turnover:
            return self.economic_bicycles_turnover * self.currency_rate
        return None
    economic_bicycles_turnover_USD.short_description = "Umsatz Fahrräder USD"

    def economic_spareparts_turnover_USD(self):
        if self.economic_spareparts_turnover:
            return self.economic_spareparts_turnover * self.currency_rate
        return None
    economic_spareparts_turnover_USD.short_description = "Umsatz Ersatzteile USD"

    def economic_services_turnover_USD(self):
        if self.economic_services_turnover:
            return self.economic_services_turnover * self.currency_rate
        return None
    economic_services_turnover_USD.short_description = "Umsatz Dienstleistungen USD"

    def economic_turnover_total_USD(self):
        if self.economic_turnover_total:
            return self.economic_turnover_total * self.currency_rate
        return None
    economic_turnover_total_USD.short_description = "Umsatz Total USD"

    def economic_transport_costs_port_to_organisation_USD(self):
        if self.economic_transport_costs_port_to_organisation:
            return self.economic_transport_costs_port_to_organisation * self.currency_rate
        return None
    economic_transport_costs_port_to_organisation_USD.short_description = "Transportkosten Hafen bis Organisation USD"

    def communityproject_reinvest_profit_total_USD(self):
        if self.communityproject_reinvest_profit_total:
            return self.communityproject_reinvest_profit_total * self.currency_rate
        return None
    communityproject_reinvest_profit_total_USD.short_description = "In Gemeinschaftsprojekt investierter Betrag USD"
    

    def get_staff(self):
        """
        Return list of staff objects.
        """
        return Staff.objects.filter(report=self.id)

    def __unicode__(self):
        return u"{}, Report vom {}".format(self.partner_sud, self.creation)
