# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sbbtracking', '0012_auto_20160329_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltracking',
            name='note',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Bemerkung', blank=True),
        ),
        migrations.AddField(
            model_name='historicaltrackingeventtype',
            name='complete_tracking',
            field=models.BooleanField(default=False, help_text=b'Gilt ein Tracking mit diesem Event als beendet?', verbose_name=b'Schliesst Tracking ab?'),
        ),
        migrations.AddField(
            model_name='tracking',
            name='note',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Bemerkung', blank=True),
        ),
        migrations.AddField(
            model_name='trackingeventtype',
            name='complete_tracking',
            field=models.BooleanField(default=False, help_text=b'Gilt ein Tracking mit diesem Event als beendet?', verbose_name=b'Schliesst Tracking ab?'),
        ),
    ]
