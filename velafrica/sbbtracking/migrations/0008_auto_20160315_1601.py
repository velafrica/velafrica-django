# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sbbtracking', '0007_auto_20160315_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltrackingevent',
            name='event_type',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='sbbtracking.TrackingEventType', null=True),
        ),
        migrations.AddField(
            model_name='trackingevent',
            name='event_type',
            field=models.ForeignKey(default=1, to='sbbtracking.TrackingEventType', help_text=b'Art des Events'),
            preserve_default=False,
        ),
    ]
