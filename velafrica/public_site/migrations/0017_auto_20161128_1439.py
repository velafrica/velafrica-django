# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-28 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_site', '0016_teammember_sorting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partner',
            name='address',
        ),
        migrations.AddField(
            model_name='partner',
            name='city',
            field=models.CharField(default='', max_length=255, verbose_name=b'Stadt'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partner',
            name='location',
            field=models.CharField(default='meep', max_length=255, verbose_name=b'Kanton/Staat'),
            preserve_default=False,
        ),
    ]
