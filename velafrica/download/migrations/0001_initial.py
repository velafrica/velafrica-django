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
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Uploadzeitpunkt')),
                ('name', models.CharField(help_text=b'Name der im Frontend angezeigt werden soll', max_length=255, verbose_name=b'Dateiname')),
                ('description', models.CharField(max_length=255, null=True, verbose_name=b'Beschreibung', blank=True)),
                ('file', models.FileField(upload_to=b'')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalFile',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Uploadzeitpunkt')),
                ('name', models.CharField(help_text=b'Name der im Frontend angezeigt werden soll', max_length=255, verbose_name=b'Dateiname')),
                ('description', models.CharField(max_length=255, null=True, verbose_name=b'Beschreibung', blank=True)),
                ('file', models.TextField(max_length=100)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical file',
            },
        ),
    ]
