# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sbbtracking', '0008_auto_20160315_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='emaillog',
            name='tracking_event',
            field=models.ForeignKey(default=1, to='sbbtracking.TrackingEvent'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalemaillog',
            name='tracking_event',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='sbbtracking.TrackingEvent', null=True),
        ),
    ]
