# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('velafrica_sud', '0004_auto_20160310_1324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='container',
            name='velos',
        ),
        migrations.RemoveField(
            model_name='historicalcontainer',
            name='velos',
        ),
        migrations.AddField(
            model_name='container',
            name='velos_loading',
            field=models.IntegerField(default=0, verbose_name=b'Anzahl Velos eingeladen'),
        ),
        migrations.AddField(
            model_name='historicalcontainer',
            name='velos_loading',
            field=models.IntegerField(default=0, verbose_name=b'Anzahl Velos eingeladen'),
        ),
    ]
