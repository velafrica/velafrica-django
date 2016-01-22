# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='note',
            field=models.TextField(null=True, verbose_name=b'Bemerkung', blank=True),
        ),
        migrations.AddField(
            model_name='historicalentry',
            name='note',
            field=models.TextField(null=True, verbose_name=b'Bemerkung', blank=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Datum und Uhrzeit'),
        ),
        migrations.AlterField(
            model_name='historicalentry',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Datum und Uhrzeit'),
        ),
    ]
