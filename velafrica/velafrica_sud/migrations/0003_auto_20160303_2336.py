# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('velafrica_sud', '0002_auto_20160303_2333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalpartnersud',
            name='city',
        ),
        migrations.RemoveField(
            model_name='historicalpartnersud',
            name='plz',
        ),
        migrations.RemoveField(
            model_name='historicalpartnersud',
            name='street',
        ),
        migrations.RemoveField(
            model_name='partnersud',
            name='city',
        ),
        migrations.RemoveField(
            model_name='partnersud',
            name='plz',
        ),
        migrations.RemoveField(
            model_name='partnersud',
            name='street',
        ),
        migrations.AddField(
            model_name='historicalpartnersud',
            name='latitude',
            field=models.IntegerField(null=True, verbose_name=b'Breitengrad', blank=True),
        ),
        migrations.AddField(
            model_name='historicalpartnersud',
            name='longitude',
            field=models.IntegerField(null=True, verbose_name=b'L\xc3\xa4ngengrad', blank=True),
        ),
        migrations.AddField(
            model_name='partnersud',
            name='latitude',
            field=models.IntegerField(null=True, verbose_name=b'Breitengrad', blank=True),
        ),
        migrations.AddField(
            model_name='partnersud',
            name='longitude',
            field=models.IntegerField(null=True, verbose_name=b'L\xc3\xa4ngengrad', blank=True),
        ),
    ]
