# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('velafrica_sud', '0006_auto_20160310_1330'),
    ]

    operations = [
        migrations.RenameField(
            model_name='container',
            old_name='velos_loading',
            new_name='velos_loaded',
        ),
        migrations.RenameField(
            model_name='historicalcontainer',
            old_name='velos_loading',
            new_name='velos_loaded',
        ),
    ]
