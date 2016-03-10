# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organisation', '0004_auto_20160218_0856'),
        ('stock', '0001_squashed_0003_stocktransfer_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalStock',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('amount', models.IntegerField(default=0, help_text=b'Anzahl der Produkte an Lager', verbose_name=b'St\xc3\xbcckzahl')),
                ('last_modified', models.DateTimeField(help_text=b'Tag und Zeit wann das Objekt zuletzt ge\xc3\xa4ndert wurde.', editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('product', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='stock.Product', null=True)),
                ('warehouse', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='stock.Warehouse', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical stock',
            },
        ),
        migrations.CreateModel(
            name='HistoricalStockTransferPosition',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('amount', models.IntegerField(verbose_name=b'St\xc3\xbcckzahl')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('product', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='stock.Product', null=True)),
                ('stocktransfer', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='stock.StockTransfer', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical stock transfer position',
            },
        ),
        migrations.CreateModel(
            name='HistoricalWarehouse',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(help_text=b'Der Name / Bezeichnung des Lagers', max_length=255, verbose_name=b'Name')),
                ('description', models.CharField(help_text=b'Beschreibung / Bemerkungen zum Lager', max_length=255, null=True, verbose_name=b'Beschreibung', blank=True)),
                ('image', models.TextField(max_length=100, null=True, verbose_name=b'Bild des Lagers', blank=True)),
                ('stock_management', models.BooleanField(default=False, help_text=b'Gibt an ob automatisches Stock-Management aktiviert ist, d.h. ob bei Stock Verschiebungen der Stock automatisch angepasst werden soll.', verbose_name=b'Automatisches Stock-Management')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('organisation', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='organisation.Organisation', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical warehouse',
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['articlenr_start', 'name'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='stock',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 10, 13, 24, 27, 983325, tzinfo=utc), help_text=b'Tag und Zeit wann das Objekt zuletzt ge\xc3\xa4ndert wurde.', auto_now=True),
            preserve_default=False,
        ),
    ]
