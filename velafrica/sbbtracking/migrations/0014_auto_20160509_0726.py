# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sbbtracking', '0013_auto_20160503_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltrackingevent',
            name='label',
            field=models.CharField(help_text=b'Text Label auf der Tracking Seite (optional)', max_length=255, null=True, verbose_name=b'Label', blank=True),
        ),
        migrations.AddField(
            model_name='trackingevent',
            name='label',
            field=models.CharField(help_text=b'Text Label auf der Tracking Seite (optional)', max_length=255, null=True, verbose_name=b'Label', blank=True),
        ),
        migrations.AlterField(
            model_name='historicaltrackingevent',
            name='note',
            field=models.CharField(help_text=b'interne Bemerkung, nirgends ersichtlich f\xc3\xbcr Spender (optional)', max_length=255, null=True, verbose_name=b'Bemerkung', blank=True),
        ),
        migrations.AlterField(
            model_name='trackingevent',
            name='note',
            field=models.CharField(help_text=b'interne Bemerkung, nirgends ersichtlich f\xc3\xbcr Spender (optional)', max_length=255, null=True, verbose_name=b'Bemerkung', blank=True),
        ),
    ]
