# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sbbtracking', '0021_auto_20160510_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltracking',
            name='complete',
            field=models.BooleanField(default=False, verbose_name=b'Tracking beendet'),
        ),
        migrations.AddField(
            model_name='tracking',
            name='complete',
            field=models.BooleanField(default=False, verbose_name=b'Tracking beendet'),
        ),
    ]
