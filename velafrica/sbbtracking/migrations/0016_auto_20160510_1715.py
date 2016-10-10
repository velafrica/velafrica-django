# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sbbtracking', '0015_auto_20160509_0738'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltracking',
            name='last_event',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='sbbtracking.TrackingEvent', null=True),
        ),
        migrations.AddField(
            model_name='tracking',
            name='last_event',
            field=models.ForeignKey(related_name='tracking_last_event', verbose_name=b'Letzter hinzugef\xc3\xbcgter Event', blank=True, to='sbbtracking.TrackingEvent', null=True),
        ),
    ]
