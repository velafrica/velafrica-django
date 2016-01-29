# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0002_auto_20160129_1010'),
        ('counter', '0002_auto_20160129_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='organisation',
            field=models.ForeignKey(default=1, verbose_name=b'Verarbeitsungsort', to='organisation.Organisation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalentry',
            name='organisation',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='organisation.Organisation', null=True),
        ),
    ]
