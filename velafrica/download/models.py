# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from velafrica.core.storage import MyStorage

fs = MyStorage()

class File(models.Model):
    """
    Represents one entry of the velocounter app.
    """
    timestamp = models.DateTimeField(blank=False, null=False, default=timezone.now, verbose_name="Uploadzeitpunkt")
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Dateiname", help_text="Name der im Frontend angezeigt werden soll")
    description = models.CharField(blank=True, null=True, max_length=255, verbose_name="Beschreibung")
    #category = models.ForeignKey(FileCategory, blank=True, null=True)
    file = models.FileField(storage=fs, upload_to='downloads/', blank=True, null=True, help_text='Select file to upload.')
    history = HistoricalRecords()

    def __str__(self):
        return u"File: {}".format(self.name)

    class Meta:
        ordering = ['name']
