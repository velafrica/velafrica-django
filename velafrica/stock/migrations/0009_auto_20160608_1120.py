# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-08 09:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0008_auto_20160601_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockchange',
            name='stocktransfer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stock.StockTransfer'),
        ),
    ]