# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 11:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0002_auto_20160317_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalcategory',
            name='category_parent',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='download.HistoricalCategory'),
        ),
    ]