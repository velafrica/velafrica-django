# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sbbtracking', '0017_auto_20160510_1718'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='trackingevent',
            unique_together=set([('event_type', 'tracking')]),
        ),
    ]
