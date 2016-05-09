# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0006_auto_20160503_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproduct',
            name='packaging_unit',
            field=models.IntegerField(null=True, verbose_name=b'Verpackungseinheit (VE)', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='packaging_unit',
            field=models.IntegerField(null=True, verbose_name=b'Verpackungseinheit (VE)', blank=True),
        ),
    ]
