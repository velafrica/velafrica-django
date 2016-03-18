# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sbbtracking', '0010_auto_20160318_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaltrackingeventtype',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='trackingeventtype',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
