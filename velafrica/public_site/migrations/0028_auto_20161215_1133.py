# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-15 10:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_site', '0027_auto_20161215_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactrequest',
            name='note',
            field=models.TextField(verbose_name=b'Nachricht'),
        ),
        migrations.AlterField(
            model_name='contactrequest',
            name='phone',
            field=models.CharField(max_length=255, verbose_name=b'Telefonnummer'),
        ),
    ]
