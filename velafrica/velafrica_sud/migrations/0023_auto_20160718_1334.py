# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-18 11:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('velafrica_sud', '0022_auto_20160718_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='booked',
            field=models.BooleanField(default=False, verbose_name=b'Container angekommen & verbucht'),
        ),
        migrations.AddField(
            model_name='historicalcontainer',
            name='booked',
            field=models.BooleanField(default=False, verbose_name=b'Container angekommen & verbucht'),
        ),
    ]
