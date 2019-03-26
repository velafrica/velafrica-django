# -*- coding: utf-8 -*-
from django.db import models

from velafrica.organisation.models import Organisation, Address


def get_default_task_status():
    """
    just here for migrations, delete later
    """
    pass


class EventCategory(models.Model):
    """
    Category of collection event.
    """
    name = models.CharField(max_length=255, help_text="Name der Kategorie", unique=True)

    def __str__(self):
        return u"{}".format(self.name)

    class Meta:
        ordering = ["-name"]
        verbose_name = "Event Kategorie"
        verbose_name_plural = "Event Kategorien"


class HostType(models.Model):
    """
    Category of collection event host.
    """
    name = models.CharField(max_length=255, help_text="Name der Veranstalter Kategorie", unique=True)

    def __str__(self):
        return u"{}".format(self.name)

    class Meta:
        verbose_name = "Veranstalter Kategorie"
        verbose_name_plural = "Veranstalter Kategorien"


class Region(models.Model):
    """
    Region
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return u"{}".format(self.name)


class Event(models.Model):
    """
    Recurring CollectionEvent
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, verbose_name="Beschreibung")
    notes = models.TextField(blank=True, null=True, verbose_name="Interne Notizen")
    region = models.ForeignKey(Region, verbose_name="Region", null=True, blank=True)
    category = models.ForeignKey(EventCategory, verbose_name="Kategorie")
    yearly = models.BooleanField(default=False, verbose_name="Jährlich wiederkehrend?")
    host = models.CharField(max_length=255, verbose_name="Veranstalter")
    host_type = models.ForeignKey(HostType, null=True, verbose_name="Veranstalter Typ")
    contact = models.CharField(max_length=255, verbose_name="Kontaktperson", null=True, blank=True)

    address = models.ForeignKey(Address, verbose_name="Adresse", blank=True, null=True)
    address_notes = models.TextField(blank=True, verbose_name="Genauer Standort")

    def __str__(self):
        return u"{}".format(self.name)

    class Meta:
        verbose_name = "Event"
        ordering = ["name"]


class Task(models.Model):
    """
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return u"{}".format(self.name)


class CollectionEvent(models.Model):
    """
    An occurrence of :model:`collection.Event` with a specific start and end date.

    This is the really interesting object holding all the information.
    """
    date_start = models.DateField()
    date_end = models.DateField()
    event = models.ForeignKey(Event)
    time = models.CharField(max_length=255, blank=True, verbose_name="Veloannahme", help_text="Zeit für Veloannahme")
    notes = models.TextField(blank=True, verbose_name="To do",
                             help_text="Sachen die noch zu erledigen sind / Weitere Infos / Bemerkungen")

    # should the event be visible on the website?
    public = models.BooleanField(default=False, verbose_name="Öffentlich",
                                 help_text="Soll der Event auf der Webseite angezeigt werden?")

    # logistics
    presence_velafrica = models.BooleanField(default=False, verbose_name="Präsenz Velafrica?")
    presence_velafrica_info = models.CharField(
        max_length=255,
        blank=True,
        help_text="Infos zur Präsenz von Velafrica am Event",
        verbose_name="Präsenz Velafrica")
    collection = models.TextField(
        blank=True,
        help_text="Infos zur Abholung der Velos",
        verbose_name="Notizen Abtransport")
    processing = models.ForeignKey(
        Organisation,
        verbose_name="Velo Verarbeitung",
        related_name="processing_organisation",
        null=True,
        blank=True)
    processing_notes = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Velo Verarbeitung Notizen",
    )
    collection_partner_vrn = models.ForeignKey(
        Organisation,
        blank=True,
        null=True,
        verbose_name="Abtransport durch VRN Partner",
        help_text="Velafrica Partner der die Velos abholt",
        related_name="collection_organisation")
    collection_partner_other = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Abtransport durch andere Organisation",
        help_text="Wenn die Velos nicht von einem Velafrica Partner abgeholt werden, bitte hier eintragen von wem")
    collection_partner_confirmed = models.BooleanField(default=False, verbose_name="Transport bestätigt?")
    intermediate_store = models.BooleanField(default=False, verbose_name="Zwischenlagerung möglich?")

    # marketing
    website = models.URLField(blank=True, help_text="Website des Events")

    # results
    feedback = models.BooleanField(default=False, verbose_name="Feedback eingeholt?")
    velo_amount = models.IntegerField(default=0, verbose_name="Anzahl Velos", help_text="Anzahl gesammelter Velos")
    people_amount = models.IntegerField(default=0, verbose_name='Anzahl Helfer vor Ort')
    hours_amount = models.IntegerField(default=0, verbose_name='Geleistete Stunden',
                                       help_text="Anzahl geleistete Stunden von allen Helfern zusammen")
    money_amount = models.IntegerField(default=0, verbose_name='Gesammeltes Geld',
                                       help_text="Betrag in CHF der am Event gesammelt wurde")
    additional_results = models.TextField(blank=True, verbose_name="weitere Resultate",
                                          help_text="Zusätzliche Resultate / Erkenntnisse, mündlichesFeedback, etc")

    material_returned = models.BooleanField(default=False, verbose_name="Material retour?")
    material_returned_notes = models.TextField(blank=True, null=True,
                                               verbose_name="Bemerkungen zu Material Retournierung")

    complete = models.BooleanField(default=False, verbose_name="Abgeschlossen")

    def get_event_name(self):
        return self.event.name

    get_event_name.short_description = "Name"

    def get_event_description(self):
        return self.event.description

    get_event_description.short_description = "Beschreibung"

    def get_event_region(self):
        return self.event.region

    get_event_region.short_description = "Region"

    def get_event_category(self):
        return self.event.category

    get_event_category.short_description = "Kategorie"

    def get_event_yearly(self):
        return self.event.yearly

    get_event_yearly.short_description = "Jährlich wiederkehrend?"

    def get_event_host(self):
        return self.event.host

    get_event_host.short_description = "Veranstalter"

    def get_event_host_type(self):
        return self.event.host_type

    get_event_host_type.short_description = "Veranstalter Kategorie"

    def get_event_contact(self):
        return self.event.contact

    get_event_contact.short_description = "Kontaktperson"

    def get_event_address(self):
        return self.event.address

    get_event_address.short_description = "Adresse"

    def get_event_address_notes(self):
        return self.event.address_notes

    get_event_address_notes.short_description = "Genauer Standort"

    address_new = models.ForeignKey(Address, verbose_name="Adresse", blank=True, null=True)
    address_notes = models.TextField(blank=True)

    def get_status_logistics(self):
        """
        Get status of logistic tasks.
        """
        if self.collection_partner_confirmed:
            return "success"
        else:
            return "danger"

    def get_status_marketing(self):
        """
        Get status of logistic tasks.
        """
        tasks_count = self.taskprogress_set.all().count()
        print(tasks_count)
        if tasks_count == 0:
            return "danger"
        else:
            success_count = 0
            for t in self.taskprogress_set.all():
                if t.status:
                    success_count += 1
            if tasks_count == success_count:
                return "success"
            else:
                return "warning"

    def get_status_results(self):
        """
        Get status of feedback tasks.
        """
        if self.feedback:
            return "success"
        return "danger"

    def __str__(self):
        return u"{} ({} bis {})".format(self.event.name, self.date_start, self.date_end)

    class Meta:
        verbose_name = "Sammelanlass"
        verbose_name_plural = "Sammelanlässe"
        ordering = ['date_start']


class TaskProgress(models.Model):
    """
    Represents the progress of a task.
    """
    collection_event = models.ForeignKey(CollectionEvent)
    task = models.ForeignKey(Task)
    notes = models.TextField(blank=True, verbose_name="Notizen")
    status = models.BooleanField(default=False, verbose_name="Erledigt?")

    def __str__(self):
        return u"{}: {}".format(self.task, self.status)

    class Meta:
        verbose_name = "Task Fortschritt"
        verbose_name_plural = "Task Fortschritte"


class Dropoff(models.Model):
    """
    Represents a dropoff (where you can drop or turn in your bike)
    """

    name = models.CharField(max_length=255, verbose_name="Name der Sammelstelle")
    active = models.BooleanField(verbose_name="Aktiv", default=True)
    sbb = models.BooleanField(verbose_name="SBB", default=False)
    contact_person = models.CharField(max_length=255, blank=True, verbose_name="Kontaktperson")
    phone_number = models.CharField(max_length=255, blank=True, verbose_name="Telefonnummer")
    temp = models.BooleanField(verbose_name="Temporär", default=False)
    temp_start = models.DateField(blank=True, null=True, verbose_name="Temporär Start")
    temp_end = models.DateField(blank=True, null=True, verbose_name="Temporär Ende")
    opening_time = models.TextField(blank=True, verbose_name="Öffnungszeiten")
    notes = models.TextField(blank=True, verbose_name="Optionale Textinfo")
    address = models.ForeignKey(Address, verbose_name="Adresse")
    custom_lat = models.CharField(max_length=255, blank=True, verbose_name="Latitude")
    custom_lon = models.CharField(max_length=255, blank=True, verbose_name="Longitude")
    pickup = models.BooleanField(verbose_name="Abholservice", default=False)
    pickup_description = models.TextField(blank=True, verbose_name="Abholservice Beschreibung")

    def __str__(self):
        return u"{} - {}".format(self.name, self.address)

    class Meta:
        verbose_name = "Abgabstelle"
        verbose_name_plural = "Abgabstellen"
