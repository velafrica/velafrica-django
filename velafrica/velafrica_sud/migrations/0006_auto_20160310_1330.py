# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('velafrica_sud', '0005_auto_20160310_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='velos_unloading',
            field=models.IntegerField(default=0, verbose_name=b'Anzahl Velos ausgeladen'),
        ),
        migrations.AddField(
            model_name='historicalcontainer',
            name='velos_unloading',
            field=models.IntegerField(default=0, verbose_name=b'Anzahl Velos ausgeladen'),
        ),
    ]
