# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sbbtracking', '0011_auto_20160318_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltrackingeventtype',
            name='email_text',
            field=models.TextField(help_text=b'Text der im Benachrichtigugsemail den den Spender geschickt wird.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='trackingeventtype',
            name='email_text',
            field=models.TextField(help_text=b'Text der im Benachrichtigugsemail den den Spender geschickt wird.', null=True, blank=True),
        ),
    ]
