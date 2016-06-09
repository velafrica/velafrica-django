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
    description = models.TextField()

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
        return c.first()
    else:
        return CollectionEventTaskStatus.objects.all()


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
    time = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    notes = models.TextField()

    presence_velafrica = models.CharField(max_length=255)
    pickup = models.CharField(max_length=255)
    processing = models.CharField(max_length=255)

    organisation_done = models.BooleanField(default=False)
    website = models.URLField()
    

    #collection_partner

    velo_amount = models.IntegerField()
    people_amount = models.IntegerField()
    hours_amount = models.IntegerField()
    additional_results = models.TextField()

    def __unicode__(self):
        return u"{}".format(self.name)

