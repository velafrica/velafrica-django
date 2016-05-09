# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sbbtracking', '0014_auto_20160509_0726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaltrackingevent',
            name='label',
        ),
        migrations.RemoveField(
            model_name='trackingevent',
            name='label',
        ),
        migrations.AddField(
            model_name='historicaltrackingeventtype',
            name='label',
            field=models.CharField(help_text=b'Text Label auf der Tracking Seite (optional)', max_length=255, null=True, verbose_name=b'Label', blank=True),
        ),
        migrations.AddField(
            model_name='trackingeventtype',
            name='label',
            field=models.CharField(help_text=b'Text Label auf der Tracking Seite (optional)', max_length=255, null=True, verbose_name=b'Label', blank=True),
        ),
    ]
