# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-13 16:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking_stations', '0007_auto_20161013_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackingstationquery',
            name='event_types',
            field=models.ManyToManyField(related_name='event_types', to='sbbtracking.TrackingEventType'),
        ),
    ]
