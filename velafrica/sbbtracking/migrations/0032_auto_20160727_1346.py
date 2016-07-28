# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-27 11:46
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sbbtracking', '0031_auto_20160719_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaltracking',
            name='number_of_velos',
        ),
        migrations.RemoveField(
            model_name='tracking',
            name='number_of_velos',
        ),
        migrations.AlterField(
            model_name='historicaltracking',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.EmailValidator], verbose_name=b'Email'),
        ),
        migrations.AlterField(
            model_name='historicaltracking',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Vorname'),
        ),
        migrations.AlterField(
            model_name='historicaltracking',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Nachname'),
        ),
        migrations.AlterField(
            model_name='tracking',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.EmailValidator], verbose_name=b'Email'),
        ),
        migrations.AlterField(
            model_name='tracking',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Vorname'),
        ),
        migrations.AlterField(
            model_name='tracking',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Nachname'),
        ),
    ]
