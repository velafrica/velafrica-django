# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-09-04 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bikes', '0002_auto_20190904_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='bike',
            name='bike_model',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Model'),
        ),
        migrations.AddField(
            model_name='bike',
            name='rear_suspension',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Rear Suspension'),
        )
    ]
