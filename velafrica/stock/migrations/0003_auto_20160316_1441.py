# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock', '0002_auto_20160310_1324'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalStockList',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('last_change', models.DateTimeField(default=datetime.datetime.now)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical stock list',
            },
        ),
        migrations.CreateModel(
            name='HistoricalStockListPosition',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('amount', models.IntegerField(verbose_name=b'St\xc3\xbcckzahl')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('product', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='stock.Product', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical stock list position',
            },
        ),
        migrations.CreateModel(
            name='HistoricalStockTransfer',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name=b'Ausf\xc3\xbchrdatum')),
                ('note', models.CharField(max_length=255, null=True, verbose_name=b'Bemerkungen', blank=True)),
                ('booked', models.BooleanField(default=False, help_text=b'Gibt an ob der Stock bereits angepasst wurde.')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('warehouse_from', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='stock.Warehouse', null=True)),
                ('warehouse_to', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='stock.Warehouse', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical stock transfer',
            },
        ),
        migrations.CreateModel(
            name='StockChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('stock_change_type', models.CharField(max_length=255, choices=[(b'out', b'out'), (b'in', b'in')])),
            ],
        ),
        migrations.CreateModel(
            name='StockList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_change', models.DateTimeField(default=datetime.datetime.now)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='StockListPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField(verbose_name=b'St\xc3\xbcckzahl')),
                ('product', models.ForeignKey(to='stock.Product')),
                ('stocklist', models.ForeignKey(verbose_name=b'StockList', to='stock.StockList')),
            ],
        ),
        migrations.RemoveField(
            model_name='historicalstocktransferposition',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalstocktransferposition',
            name='product',
        ),
        migrations.RemoveField(
            model_name='historicalstocktransferposition',
            name='stocktransfer',
        ),
        migrations.AlterUniqueTogether(
            name='stocktransferposition',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='stocktransferposition',
            name='product',
        ),
        migrations.RemoveField(
            model_name='stocktransferposition',
            name='stocktransfer',
        ),
        migrations.RemoveField(
            model_name='stocktransfer',
            name='executor',
        ),
        migrations.DeleteModel(
            name='HistoricalStockTransferPosition',
        ),
        migrations.DeleteModel(
            name='StockTransferPosition',
        ),
        migrations.AddField(
            model_name='stockchange',
            name='stocklist',
            field=models.ForeignKey(to='stock.StockList'),
        ),
        migrations.AddField(
            model_name='stockchange',
            name='stocktransfer',
            field=models.ForeignKey(to='stock.StockTransfer'),
        ),
        migrations.AddField(
            model_name='stockchange',
            name='warehouse',
            field=models.ForeignKey(to='stock.Warehouse'),
        ),
        migrations.AddField(
            model_name='historicalstocklistposition',
            name='stocklist',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='stock.StockList', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='stocklistposition',
            unique_together=set([('stocklist', 'product')]),
        ),
    ]
