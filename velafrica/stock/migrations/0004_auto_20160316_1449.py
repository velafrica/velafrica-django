# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_auto_20160316_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalstocktransfer',
            name='stocklist',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='stock.StockList', null=True),
        ),
        migrations.AddField(
            model_name='stocktransfer',
            name='stocklist',
            field=models.ForeignKey(default=1, verbose_name=b'Stock List', to='stock.StockList'),
            preserve_default=False,
        ),
    ]
