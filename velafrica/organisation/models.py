from django.core.validators import RegexValidator
from django.db import models
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords

class Organisation(models.Model):
    """
    Represents a network partner.
    TODO:
    - name
    - Adresse
    - Kontaktperson (Vorname / Nachname)
    - Tel
    - Email
    - Bemerkungen
    - Website
    """
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Name der Organisation")
    street = models.CharField(blank=False, null=False, max_length=255, verbose_name="Strasse")
    plz = models.IntegerField(blank=False, null=False, verbose_name="PLZ")
    city = models.CharField(blank=False, null=False, max_length=255, verbose_name="Ort")

    website = models.CharField(blank=True, null=True, max_length=255, verbose_name="Website")

    history = HistoricalRecords()

    def __unicode__(self):
        return "{}, {}".format(self.name, self.city)

    class Meta:
        ordering = ['name']
