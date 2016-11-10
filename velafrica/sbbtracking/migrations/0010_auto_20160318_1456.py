# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_resized.forms
from django.db import models, migrations

import velafrica.core.storage


class Migration(migrations.Migration):

    dependencies = [
        ('sbbtracking', '0009_auto_20160315_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltrackingeventtype',
            name='image',
            field=models.TextField(max_length=100, null=True, verbose_name=b'Symbolbild', blank=True),
        ),
        migrations.AddField(
            model_name='trackingeventtype',
            name='image',
            field=django_resized.forms.ResizedImageField(storage=velafrica.core.storage.MyStorage(), upload_to=b'tracking/eventtypes/', null=True, verbose_name=b'Symbolbild', blank=True),
        ),
    ]
