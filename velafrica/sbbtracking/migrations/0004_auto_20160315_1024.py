# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sbbtracking', '0003_auto_20160315_1011'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tracking',
            options={'ordering': ['-tracking_no']},
        ),
        migrations.RenameField(
            model_name='historicaltracking',
            old_name='trackingno',
            new_name='tracking_no',
        ),
        migrations.RenameField(
            model_name='tracking',
            old_name='trackingno',
            new_name='tracking_no',
        ),
    ]
