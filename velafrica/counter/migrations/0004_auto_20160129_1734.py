# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0003_auto_20160129_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateField(default=datetime.datetime.now, verbose_name=b'Datum'),
        ),
        migrations.AlterField(
            model_name='historicalentry',
            name='date',
            field=models.DateField(default=datetime.datetime.now, verbose_name=b'Datum'),
        ),
    ]
