# apps.py
from django.apps import AppConfig

class MyAppConfig(AppConfig):

    # name needs to be the same as it should be to import the app in INSTALLED_APPS
    name = 'velafrica.stock'
    verbose_name = 'Stock Management'

    def ready(self):
        # import signal handlers
        import velafrica.stock.signals.handlers
