# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from simple_history.models import HistoricalRecords

from velafrica.core.ftp import MyFTPStorage
fs = MyFTPStorage()

class Category(models.Model):
    """
    Represents a file Category
    """
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Name", help_text="Name der im Frontend angezeigt werden soll")
    description = models.CharField(blank=True, null=True, max_length=255, verbose_name="Beschreibung")
    category_parent = models.ForeignKey('self', help_text="Übergeordnete Kategorie")
    history = HistoricalRecords()

    def __unicode__(self):
        return u"File: {}".format(self.name)

    class Meta:
        ordering = ['name']


class File(models.Model):
    """
    Represents one entry of the velocounter app.
    """
    timestamp = models.DateTimeField(blank=False, null=False, default=datetime.now, verbose_name="Uploadzeitpunkt")
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Dateiname", help_text="Name der im Frontend angezeigt werden soll")
    description = models.CharField(blank=True, null=True, max_length=255, verbose_name="Beschreibung")
    category = models.ForeignKey(Category, blank=True, null=True)
    file = models.FileField(storage=fs, upload_to='downloads/', blank=True, null=True, help_text='Select file to upload.')
    history = HistoricalRecords()

    def __unicode__(self):
        return u"File: {}".format(self.name)

    class Meta:
        ordering = ['name']
