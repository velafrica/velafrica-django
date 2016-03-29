# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('velafrica_sud', '0009_auto_20160317_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpartnersud',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='partnersud',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
