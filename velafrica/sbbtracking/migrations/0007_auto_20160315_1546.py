# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sbbtracking', '0006_emaillog_historicalemaillog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaltrackingeventtype',
            name='description',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='trackingeventtype',
            name='description',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
