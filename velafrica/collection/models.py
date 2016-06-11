# -*- coding: utf-8 -*-
from datetime import timedelta, date
from django.utils import timezone
from django.db import models
from simple_history.models import HistoricalRecords
from velafrica.organisation.models import Organisation, Municipality

# Create your models here.
"""
class EventContext(models.Model):
    
    Todo: write doc.
    
    name
    description
    history = HistoricalRecords()

    def __unicode__(self):
        return u"{}: {}".format(self.date, self.amount)

    class Meta:
        unique_together = ['organisation', 'date']
        verbose_name_plural = "Entries"
        ordering = ['-date']
    """

class EventType(models.Model):
    """
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"{}".format(self.name)


class CollectionPartner(models.Model):
    """
    """
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u"{}".format(self.name)    


class Task(models.Model):
    """
    """
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u"{}".format(self.name)        


class TaskStatus(models.Model):
    """
    """
    name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            TaskStatus.objects.all().update(**{'is_default': False})
        super(TaskStatus, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

def get_default_task_status():
    """
    Get the default value
    """
    c = TaskStatus.objects.filter(is_default=True)
    if c:
        return c.first().id
    else:
        return None


class EventType(models.Model):
    """
    """
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Event(models.Model):
    """
    """
    date_start = models.DateField()
    date_end = models.DateField()
    municipality = models.ForeignKey(Municipality)
    type = models.ForeignKey(EventType)
    time = models.CharField(max_length=255, blank=True, help_text="Zeit für Veloannahme")
    host = models.CharField(max_length=255, blank=True, help_text="Veranstalter des Sammelanlasses")
    notes = models.TextField(blank=True, help_text="Weitere Infos / Bemerkungen")

    presence_velafrica = models.CharField(max_length=255, blank=True, help_text="Infos zur Präsenz von Velafrica am Event")
    pickup = models.CharField(max_length=255, blank=True, help_text="Infos zur Abholung der Velos")
    processing = models.CharField(max_length=255, help_text="Infos zur Verarbeitung der gesammelten Velos")

    collection_type = models.CharField(max_length=255, blank=True)
    collection_partner = models.ForeignKey(CollectionPartner, blank=True, null=True)
    feedback = models.TextField(max_length=255, blank=True)

    website = models.URLField(blank=True, help_text="Website des Events")
    

    #collection_partner

    velo_amount = models.IntegerField(default=0)
    people_amount = models.IntegerField(default=0)
    hours_amount = models.IntegerField(default=0)
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
    event = models.ForeignKey(Event)
    task = models.ForeignKey(Task)
    notes = models.TextField()
    status = models.ForeignKey(TaskStatus, blank=True, null=True, default=get_default_task_status)

    def __unicode__(self):
        return u"{}: {}".format(self.task, self.status)