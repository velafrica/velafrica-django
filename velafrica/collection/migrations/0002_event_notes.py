# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-03-26 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name=b'Interne Notizen'),
        ),
    ]
