# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_auto_20160202_1434'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stock',
            unique_together=set([('product', 'warehouse')]),
        ),
        migrations.AlterUniqueTogether(
            name='stocktransferposition',
            unique_together=set([('stocktransfer', 'product')]),
        ),
    ]
