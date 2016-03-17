# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_resized.forms
import velafrica.core.ftp


class Migration(migrations.Migration):

    dependencies = [
        ('velafrica_sud', '0008_auto_20160310_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='flag',
            field=django_resized.forms.ResizedImageField(help_text=b'Flagge des Landes.', storage=velafrica.core.ftp.MyFTPStorage(), null=True, upload_to=b'velafrica_sud/country/flags/', blank=True),
        ),
    ]
