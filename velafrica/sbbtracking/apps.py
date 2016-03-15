# apps.py
from django.apps import AppConfig

class MyAppConfig(AppConfig):

	# name needs to be the same as it should be to import the app in INSTALLED_APPS
    name = 'velafrica.sbbtracking'
    verbose_name = 'SBB Tracking'

    def ready(self):
        # import signal handlers
        import velafrica.sbbtracking.signals.handlers