# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('velafrica_sud', '0003_auto_20160303_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='logistics',
            field=models.ForeignKey(to='velafrica_sud.Forwarder', max_length=255, blank=True, help_text=b'Logistikunternehmen', null=True, verbose_name=b'Forwarder'),
        ),
    ]
