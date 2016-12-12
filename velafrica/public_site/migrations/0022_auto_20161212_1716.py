# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-12 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_site', '0021_eventdatetime'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventdatetime',
            options={'ordering': ['date'], 'verbose_name': 'Datum/Uhrzeit'},
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, verbose_name=b'Beschreibung'),
        ),
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.CharField(blank=True, max_length=255, verbose_name=b'Veranstalter'),
        ),
    ]
