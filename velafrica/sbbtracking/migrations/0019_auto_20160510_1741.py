# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sbbtracking', '0018_auto_20160510_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracking',
            name='last_event',
            field=models.ForeignKey(related_name='tracking_last_event', verbose_name=b'Letzter Event', blank=True, to='sbbtracking.TrackingEvent', null=True),
        ),
    ]
