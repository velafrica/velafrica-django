# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.db.models.deletion
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalTracking',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('trackingno', models.CharField(max_length=10, verbose_name=b'Tracking Nummer', db_index=True)),
                ('number_of_velos', models.IntegerField(default=0)),
                ('first_name', models.CharField(max_length=255, verbose_name=b'Vorname')),
                ('last_name', models.CharField(max_length=255, verbose_name=b'Nachname')),
                ('street', models.CharField(max_length=255, null=True, verbose_name=b'Strasse', blank=True)),
                ('plz', models.IntegerField(null=True, verbose_name=b'Postleitzahl', blank=True)),
                ('town', models.CharField(max_length=255, verbose_name=b'Stadt')),
                ('email', models.CharField(max_length=255, verbose_name=b'Email', validators=[django.core.validators.EmailValidator])),
                ('tel', models.CharField(max_length=255, verbose_name=b'Telefonnummer')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical tracking',
            },
        ),
        migrations.CreateModel(
            name='HistoricalTrackingEvent',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Zeitpunkt')),
                ('note', models.CharField(max_length=255, null=True, verbose_name=b'Bemerkung', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical tracking event',
            },
        ),
        migrations.CreateModel(
            name='HistoricalTrackingEventState',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name=b'Name', blank=True)),
                ('description', models.CharField(max_length=255, null=True, verbose_name=b'Beschreibung', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical tracking event state',
            },
        ),
        migrations.CreateModel(
            name='Tracking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('trackingno', models.CharField(unique=True, max_length=10, verbose_name=b'Tracking Nummer')),
                ('number_of_velos', models.IntegerField(default=0)),
                ('first_name', models.CharField(max_length=255, verbose_name=b'Vorname')),
                ('last_name', models.CharField(max_length=255, verbose_name=b'Nachname')),
                ('street', models.CharField(max_length=255, null=True, verbose_name=b'Strasse', blank=True)),
                ('plz', models.IntegerField(null=True, verbose_name=b'Postleitzahl', blank=True)),
                ('town', models.CharField(max_length=255, verbose_name=b'Stadt')),
                ('email', models.CharField(max_length=255, verbose_name=b'Email', validators=[django.core.validators.EmailValidator])),
                ('tel', models.CharField(max_length=255, verbose_name=b'Telefonnummer')),
            ],
            options={
                'ordering': ['-trackingno'],
            },
        ),
        migrations.CreateModel(
            name='TrackingEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Zeitpunkt')),
                ('note', models.CharField(max_length=255, null=True, verbose_name=b'Bemerkung', blank=True)),
            ],
            options={
                'ordering': ['-datetime'],
            },
        ),
        migrations.CreateModel(
            name='TrackingEventState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name=b'Name', blank=True)),
                ('description', models.CharField(max_length=255, null=True, verbose_name=b'Beschreibung', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='trackingevent',
            name='state',
            field=models.ForeignKey(to='sbbtracking.TrackingEventState'),
        ),
        migrations.AddField(
            model_name='trackingevent',
            name='tracking',
            field=models.ForeignKey(to='sbbtracking.Tracking'),
        ),
        migrations.AddField(
            model_name='historicaltrackingevent',
            name='state',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='sbbtracking.TrackingEventState', null=True),
        ),
        migrations.AddField(
            model_name='historicaltrackingevent',
            name='tracking',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='sbbtracking.Tracking', null=True),
        ),
    ]
