from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

app = Celery('velafrica.core',
             broker='amqp://guest@localhost',
             backend='amqp://guest@localhost')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

from django.conf import settings  # noqa

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if __name__ == '__main__':
    app.start()
