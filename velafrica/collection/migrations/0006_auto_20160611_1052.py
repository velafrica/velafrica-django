# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-11 08:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0005_event_municipality'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='from_date',
            new_name='date_end',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='to_date',
            new_name='date_start',
        ),
        migrations.AddField(
            model_name='event',
            name='collectionpartner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='collection.CollectionPartner'),
        ),
        migrations.AddField(
            model_name='taskprogress',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='collection.Event'),
            preserve_default=False,
        ),
    ]
