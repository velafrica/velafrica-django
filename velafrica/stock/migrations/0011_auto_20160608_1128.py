# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-08 09:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0010_auto_20160608_1120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalstocktransfer',
            name='stocklist',
        ),
        migrations.RemoveField(
            model_name='stocktransfer',
            name='stocklist',
        ),
        migrations.AddField(
            model_name='historicalstocklist',
            name='stocktransfer',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='stock.StockTransfer'),
        ),
        migrations.AddField(
            model_name='stocklist',
            name='stocktransfer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.StockTransfer'),
        ),
    ]