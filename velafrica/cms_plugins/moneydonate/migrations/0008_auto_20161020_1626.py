# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-20 14:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moneydonate', '0007_auto_20161020_1619'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoiceorder',
            old_name='amount',
            new_name='donation_amount',
        ),
    ]