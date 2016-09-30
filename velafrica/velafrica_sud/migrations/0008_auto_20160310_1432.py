# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('velafrica_sud', '0007_auto_20160310_1430'),
    ]

    operations = [
        migrations.RenameField(
            model_name='container',
            old_name='velos_unloading',
            new_name='velos_unloaded',
        ),
        migrations.RenameField(
            model_name='historicalcontainer',
            old_name='velos_unloading',
            new_name='velos_unloaded',
        ),
    ]
