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
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(EventCategory)
    host = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    yearly = models.BooleanField(default=False, verbose_name="Jährlich wiederkehrend?")

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
    municipality = models.ForeignKey(Municipality)
    event = models.ForeignKey(Event)
    time = models.CharField(max_length=255, blank=True, help_text="Zeit für Veloannahme")
    host = models.CharField(max_length=255, blank=True, help_text="Veranstalter des Sammelanlasses")
    notes = models.TextField(blank=True, help_text="Weitere Infos / Bemerkungen")

    # logistics
    presence_velafrica = models.CharField(max_length=255, blank=True, help_text="Infos zur Präsenz von Velafrica am Event")
    pickup = models.CharField(max_length=255, blank=True, help_text="Infos zur Abholung der Velos")
    processing = models.CharField(max_length=255, help_text="Infos zur Verarbeitung der gesammelten Velos")
    collection_partner_vrn = models.ForeignKey(Organisation, blank=True, null=True, help_text="Velafrica Partner der die Velos abholt")
    collection_partner_other = models.CharField(max_length=255, blank=True, help_text="Wenn die Velos nicht von einem Velafrica Partner abgeholt werden, bitte hier eintragen von wem")

    # marketing
    website = models.URLField(blank=True, help_text="Website des Events")

    # results
    feedback = models.BooleanField(default=False, verbose_name="Feedback eingeholt?")
    velo_amount = models.IntegerField(default=0, verbose_name="Anzahl gesammelte Velos")
    people_amount = models.IntegerField(default=0, verbose_name='Anzahl Helfer vor Ort')
    hours_amount = models.IntegerField(default=0, verbose_name='Geleistete Stunden', help_text="Anzahl geleistete Stunden von allen Helfern zusammen")
    additional_results = models.TextField(blank=True, help_text="Zusätzliche Resultate / Erkenntnisse")

    def get_task_progress_summary_string(self):
        result = ""
        tp = TaskProgress.objects.all()
        for t in tp:
            result += "{}: {}\n".format(t.task.name, t.status.name)
        return result

    def __unicode__(self):
        return u"{} bis {} in {}".format(self.date_start, self.date_end, self.municipality.plz_name)


class TaskProgress(models.Model):
    """
    """
    collection_event = models.ForeignKey(CollectionEvent)
    task = models.ForeignKey(Task)
    notes = models.TextField(blank=True)
    status = models.BooleanField(default=False)

    def __unicode__(self):
        return u"{}: {}".format(self.task, self.status)