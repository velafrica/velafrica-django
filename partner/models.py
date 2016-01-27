from django.core.validators import RegexValidator
from django.db import models
from django_resized import ResizedImageField
from simple_history.models import HistoricalRecords

class Partner(models.Model):
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
    """
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name="Kategoriebezeichnung")
    description = models.TextField(blank=True, null=True, verbose_name="Beschreibung")
    image = ResizedImageField(size=[500, 500], upload_to='stock/categories/', blank=True, null=True, help_text='Product picture.')
    color = models.CharField(
        validators=[
            RegexValidator(
                regex="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", 
                message="Must be a hexcode (e.g. #000 or #000000)",
                code="invalid_hexcode"
            )
        ],
        help_text="Colour code to use for this category (hex value, i.e. #000 or #000000)",
        blank=True,
        null=True,
        max_length=7
    )
    history = HistoricalRecords()

    def __unicode__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    """