# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Datum und Uhrzeit')),
                ('amount', models.IntegerField(verbose_name=b'Anzahl Velos')),
                ('note', models.TextField(null=True, verbose_name=b'Bemerkung', blank=True)),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name_plural': 'Entries',
            },
        ),
        migrations.CreateModel(
            name='HistoricalEntry',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Datum und Uhrzeit')),
                ('amount', models.IntegerField(verbose_name=b'Anzahl Velos')),
                ('note', models.TextField(null=True, verbose_name=b'Bemerkung', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical entry',
            },
        ),
    ]
