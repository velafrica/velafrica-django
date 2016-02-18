# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.
class File(models.Model):
    """
    Represents one entry of the velocounter app.
    """
    timestamp = models.DateTimeField(blank=False, null=False, default=datetime.now, verbose_name="Uploadzeitpunkt")
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Dateiname", help_text="Name der im Frontend angezeigt werden soll")
    description = models.CharField(blank=True, null=True, max_length=255, verbose_name="Beschreibung")
    file = models.FileField()
    history = HistoricalRecords()

    def __unicode__(self):
        return u"File: {}".format(self.name)

    class Meta:
        ordering = ['name']
