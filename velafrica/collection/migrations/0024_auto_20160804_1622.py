# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-04 14:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0023_auto_20160804_1615'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='address_new',
            new_name='address',
        ),
    ]