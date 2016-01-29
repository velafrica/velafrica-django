from datetime import datetime    
from django.db import models
from simple_history.models import HistoricalRecords
from velafrica.organisation.models import Organisation

# Create your models here.
class Entry(models.Model):
    """
    Represents one entry of the velocounter app.
    """
    date = models.DateTimeField(blank=False, null=False, default=datetime.now, verbose_name="Datum und Uhrzeit")
    organisation = models.ForeignKey(Organisation, blank=False, null=False, verbose_name="Verarbeitsungsort")
    amount = models.IntegerField(blank=False, null=False, verbose_name="Anzahl Velos")
    note = models.CharField(blank=True, null=True, max_length=255, verbose_name="Bemerkungen")
    history = HistoricalRecords()

    def __unicode__(self):
        return "{}: {}".format(self.date, self.amount)

    class Meta:
        verbose_name_plural = "Entries"
        ordering = ['-date']
