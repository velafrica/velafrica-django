# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import velafrica.core.ftp


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0001_squashed_0003_auto_20160222_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(help_text=b'Select file to upload.', storage=velafrica.core.ftp.MyFTPStorage(), null=True, upload_to=b'downloads/', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalfile',
            name='file',
            field=models.TextField(help_text=b'Select file to upload.', max_length=100, null=True, blank=True),
        ),
    ]
