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

class CollectionEventType(models.Model):
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


class CollectionEventTask(models.Model):
    """
    """
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u"{}".format(self.name)        


class CollectionEventTaskStatus(models.Model):
    """
    """
    name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            CollectionEventTaskStatus.objects.all().update(**{'is_default': False})
        super(CollectionEventTaskStatus, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

def get_default_task_status():
    """
    Get the default value
    """
    c = CollectionEventTaskStatus.objects.filter(is_default=True)
    if c:
        return c.first().id
    else:
        return None


class CollectionEventTaskProgress(models.Model):
    """
    """
    task = models.ForeignKey(CollectionEventTask)
    notes = models.TextField()
    status = models.ForeignKey(CollectionEventTaskStatus, blank=True, null=True, default=get_default_task_status)

    def __unicode__(self):
        return u"{}".format(self.name)


class CollectionEvent(models.Model):
    """
    """
    from_date = models.DateField()
    to_date = models.DateField()
    ort = models.ForeignKey(Municipality)
    time = models.CharField(max_length=255, blank=True, help_text="Zeit für Veloannahme")
    host = models.CharField(max_length=255, blank=True, help_text="Veranstalter des Sammelanlasses")
    notes = models.TextField(blank=True, help_text="Weitere Infos / Bemerkungen")

    presence_velafrica = models.CharField(max_length=255, blank=True, help_text="Infos zur Präsenz von Velafrica am Event")
    pickup = models.CharField(max_length=255, blank=True, help_text="Infos zur Abholung der Velos")
    processing = models.CharField(max_length=255, help_text="Infos zur Verarbeitung der gesammelten Velos")

    organisation_done = models.BooleanField(default=False)
    website = models.URLField(blank=True, help_text="Website des Events")
    

    #collection_partner

    velo_amount = models.IntegerField(default=0)
    people_amount = models.IntegerField(default=0)
    hours_amount = models.IntegerField(default=0)
    additional_results = models.TextField(blank=True, help_text="Zusätzliche Resultate / Erkenntnisse")

    def __unicode__(self):
        return u"{}".format(self.name)

