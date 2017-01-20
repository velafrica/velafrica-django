from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from django.db import models


class BigPicture(CMSPlugin):
    background_img = FilerImageField(null=True, blank=True, related_name="background")
    header = models.CharField(max_length=100, null=True, blank=True)
    text = models.CharField(max_length=500, null=True, blank=True)
    min_height = models.IntegerField(default=500, null=False, blank=False)