# -*- coding: utf-8 -*-
# apps.py
from django.apps import AppConfig


class BikeAppConfig(AppConfig):

    # name needs to be the same as it should be to import the app in INSTALLED_APPS
    name = 'velafrica.bikes'
    verbose_name = u"Velafrica Bikes"

    # def ready(self):
    #   import signal handlers
