# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-03 12:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0030_auto_20160729_0848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalproduct',
            name='purchase_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='purchase_price',
        ),
    ]