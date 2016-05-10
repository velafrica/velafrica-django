# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sbbtracking', '0019_auto_20160510_1741'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaltracking',
            name='completed',
        ),
        migrations.RemoveField(
            model_name='historicaltracking',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='historicaltracking',
            name='ready_for_export',
        ),
        migrations.RemoveField(
            model_name='tracking',
            name='completed',
        ),
        migrations.RemoveField(
            model_name='tracking',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='tracking',
            name='ready_for_export',
        ),
    ]
