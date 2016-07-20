# -*- coding: utf-8 -*-
# apps.py
from django.apps import AppConfig

class MyAppConfig(AppConfig):

	# name needs to be the same as it should be to import the app in INSTALLED_APPS
    name = 'velafrica.velafrica_sud'
    verbose_name = u"Velafrica Sud"

    def ready(self):
        # import signal handlers
        import velafrica.velafrica_sud.signals.handlers