# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_auto_20160317_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproduct',
            name='name_en',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Produktbezeichnung EN', blank=True),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='name_fr',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Produktbezeichnung FR', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_en',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Produktbezeichnung EN', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_fr',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Produktbezeichnung FR', blank=True),
        ),
    ]
