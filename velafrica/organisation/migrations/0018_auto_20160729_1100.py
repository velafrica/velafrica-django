# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-29 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0017_auto_20160729_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='code',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name=b'L\xc3\xa4ndercode (ISO 3166-1 alpha-2)'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name=b'Name des Landes'),
        ),
    ]
