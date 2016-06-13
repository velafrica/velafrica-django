# -*- coding: utf-8 -*-
from datetime import timedelta, date
from django.utils import timezone
from django.db import models
from simple_history.models import HistoricalRecords
from velafrica.organisation.models import Organisation, Municipality

def get_default_task_status():
    """
    just here for migrations, delete later
    """
    pass


class EventCategory(models.Model):
    """
    """
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u"{}".format(self.name)


class Event(models.Model):
    """
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, verbose_name="Beschreibung")
    category = models.ForeignKey(EventCategory, verbose_name="Kategorie")
    yearly = models.BooleanField(default=False, verbose_name="Jährlich wiederkehrend?")
    host = models.CharField(max_length=255, verbose_name="Veranstalter")
    municipality = models.ForeignKey(Municipality, verbose_name="Ort")
    address = models.TextField(blank=True)

    def __unicode__(self):
        return u"{}".format(self.name)


class Task(models.Model):
    """
    """
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u"{}".format(self.name)


class CollectionEvent(models.Model):
    """
    """
    date_start = models.DateField()
    date_end = models.DateField()
    event = models.ForeignKey(Event)
    time = models.CharField(max_length=255, blank=True, verbose_name="Veloannahme", help_text="Zeit für Veloannahme")
    notes = models.TextField(blank=True, verbose_name="weitere Infos", help_text="Weitere Infos / Bemerkungen")

    # logistics
    presence_velafrica = models.TextField(
        blank=True, 
        help_text="Infos zur Präsenz von Velafrica am Event",
        verbose_name="Präsenz Velafrica")
    pickup = models.TextField(
        blank=True,
        help_text="Infos zur Abholung der Velos",
        verbose_name="Abtransport")
    processing = models.TextField(
        blank=True,
        help_text="Infos zur Verarbeitung der gesammelten Velos",
        verbose_name="Velo Verarbeitung")
    collection_partner_vrn = models.ForeignKey(
        Organisation, 
        blank=True, 
        null=True,
        verbose_name="Abtransport durch VRN Partner",
        help_text="Velafrica Partner der die Velos abholt")
    collection_partner_other = models.CharField(
        max_length=255, 
        blank=True, 
        verbose_name="Abtransport durch andere Organisation",
        help_text="Wenn die Velos nicht von einem Velafrica Partner abgeholt werden, bitte hier eintragen von wem")
    collection_partner_confirmed = models.BooleanField(default=False)

    # marketing
    website = models.URLField(blank=True, help_text="Website des Events")

    # results
    feedback = models.BooleanField(default=False, verbose_name="Feedback eingeholt?")
    velo_amount = models.IntegerField(default=0, verbose_name="Anzahl gesammelte Velos")
    people_amount = models.IntegerField(default=0, verbose_name='Anzahl Helfer vor Ort')
    hours_amount = models.IntegerField(default=0, verbose_name='Geleistete Stunden', help_text="Anzahl geleistete Stunden von allen Helfern zusammen")
    additional_results = models.TextField(blank=True, verbose_name="weitere Resultate", help_text="Zusätzliche Resultate / Erkenntnisse")

    def get_status_logistics(self):
        pass

    def get_status_marketing(self):
        pass

    def get_status_results(self):
        pass

    def __unicode__(self):
        return u"{} ({} bis {})".format(self.event.name, self.date_start, self.date_end)


class TaskProgress(models.Model):
    """
    """
    collection_event = models.ForeignKey(CollectionEvent)
    task = models.ForeignKey(Task)
    notes = models.TextField(blank=True, verbose_name="Notizen")
    status = models.BooleanField(default=False, verbose_name="Erledigt?")

    def __unicode__(self):
        return u"{}: {}".format(self.task, self.status)