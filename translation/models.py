from django.db import models
from simple_history.models import HistoricalRecords

class Language(models.Model):
    """
    Represents a language.
    """
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Sprache")
    short = models.CharField(blank=False, null=False, max_length=2, verbose_name="Kuerzel")
    history = HistoricalRecords()

    def __unicode__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ['name']
