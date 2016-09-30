# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import django.db.models.deletion
import django_resized.forms
from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_squashed_0003_stocktransfer_note'),
        ('organisation', '0003_auto_20160202_1454'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name=b'Name des Fahrzeugs')),
                ('image', django_resized.forms.ResizedImageField(help_text=b'Foto des Fahrzeugs', null=True, upload_to=b'stock/categories/', blank=True)),
                ('plate', models.CharField(max_length=255, null=True, verbose_name=b'Autokennzeichen', blank=True)),
                ('organisation', models.ForeignKey(blank=True, to='organisation.Organisation', help_text=b'Organisation welcher das Fahrzeug geh\xc3\xb6rt.', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Name des Fahrers')),
                ('organisation', models.ForeignKey(blank=True, to='organisation.Organisation', help_text=b'Organisation bei welcher der Fahrer angestellt ist.', null=True)),
                ('person', models.ForeignKey(verbose_name=b'Verkn\xc3\xbcpfte Person', blank=True, to='organisation.Person', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalCar',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name=b'Name des Fahrzeugs')),
                ('image', models.TextField(help_text=b'Foto des Fahrzeugs', max_length=100, null=True, blank=True)),
                ('plate', models.CharField(max_length=255, null=True, verbose_name=b'Autokennzeichen', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('organisation', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='organisation.Organisation', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical car',
            },
        ),
        migrations.CreateModel(
            name='HistoricalRide',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name=b'Datum')),
                ('velos', models.IntegerField(default=0, verbose_name=b'Anzahl Velos')),
                ('spare_parts', models.BooleanField(default=False, verbose_name=b'Ersatzteile transportiert?')),
                ('note', models.CharField(help_text=b'Bemerkung zur Fahrt', max_length=255, null=True, verbose_name=b'Bemerkung', blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('car', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='transport.Car', null=True)),
                ('driver', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='transport.Driver', null=True)),
                ('from_warehouse', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='stock.Warehouse', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('to_warehouse', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='stock.Warehouse', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical ride',
            },
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name=b'Datum')),
                ('velos', models.IntegerField(default=0, verbose_name=b'Anzahl Velos')),
                ('spare_parts', models.BooleanField(default=False, verbose_name=b'Ersatzteile transportiert?')),
                ('note', models.CharField(help_text=b'Bemerkung zur Fahrt', max_length=255, null=True, verbose_name=b'Bemerkung', blank=True)),
                ('car', models.ForeignKey(verbose_name=b'Fahrzeug', to='transport.Car')),
                ('driver', models.ForeignKey(verbose_name=b'Fahrer', to='transport.Driver', help_text=b'Person die den Transport durchgef\xc3\xbchrt hat.')),
                ('from_warehouse', models.ForeignKey(related_name='from_warehouse', verbose_name=b'Start', to='stock.Warehouse', help_text=b'Start der Fahrt')),
                ('to_warehouse', models.ForeignKey(related_name='to_warehouse', verbose_name=b'Ziel', to='stock.Warehouse', help_text=b'Ziel der Fahrt')),
            ],
            options={
                'ordering': ['date', 'from_warehouse'],
            },
        ),
        migrations.CreateModel(
            name='VeloState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, verbose_name=b'Name des Zustandes')),
                ('description', models.CharField(max_length=255, null=True, verbose_name=b'Beschreibung', blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='ride',
            name='velo_state',
            field=models.ForeignKey(verbose_name=b'Zustand der Velos', to='transport.VeloState'),
        ),
        migrations.AddField(
            model_name='historicalride',
            name='velo_state',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='transport.VeloState', null=True),
        ),
    ]
