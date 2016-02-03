# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_remove_stocktransfer_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocktransfer',
            name='note',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Bemerkungen', blank=True),
        ),
    ]
