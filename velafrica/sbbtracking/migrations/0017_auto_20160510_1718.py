# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sbbtracking', '0016_auto_20160510_1715'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='trackingevent',
            unique_together=set([]),
        ),
    ]
