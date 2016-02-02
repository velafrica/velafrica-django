# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0002_auto_20160129_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalorganisation',
            name='city',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Ort', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalorganisation',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Name der Organisation'),
        ),
        migrations.AlterField(
            model_name='historicalorganisation',
            name='plz',
            field=models.IntegerField(null=True, verbose_name=b'PLZ', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalorganisation',
            name='street',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Strasse', blank=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='city',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Ort', blank=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Name der Organisation'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='plz',
            field=models.IntegerField(null=True, verbose_name=b'PLZ', blank=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='street',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Strasse', blank=True),
        ),
    ]
