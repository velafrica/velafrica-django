# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-12 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_site', '0019_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='active',
            field=models.BooleanField(default=True, verbose_name=b'Aktiv'),
        ),
    ]